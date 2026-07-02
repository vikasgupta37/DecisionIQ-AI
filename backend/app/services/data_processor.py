import csv
import io
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from backend.app.schemas.processing import ColumnStats, DataQualityReport

logger = logging.getLogger(__name__)

# Supported structured formats for full processing
PROCESSABLE_EXTENSIONS = {"csv", "json", "xlsx", "xls"}


@dataclass
class ProcessingResult:
    """Internal result from the processing pipeline."""
    original_row_count: int = 0
    cleaned_row_count: int = 0
    duplicates_removed: int = 0
    nulls_filled: int = 0
    quality_report: Optional[DataQualityReport] = None
    column_stats: List[ColumnStats] = field(default_factory=list)
    log_messages: List[str] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None


class DataProcessorService:
    """
    Four-stage data processing pipeline:
    1. Validation — Check structural integrity
    2. Cleaning — Remove duplicates, handle nulls
    3. Normalization — Standardize strings, trim whitespace
    4. Statistics — Compute per-column stats and quality metrics
    """

    def process_csv(self, content: bytes) -> ProcessingResult:
        """Process CSV file content through the full pipeline."""
        result = ProcessingResult()
        try:
            text = content.decode("utf-8", errors="replace")
            reader = csv.reader(io.StringIO(text))
            all_rows = list(reader)

            if len(all_rows) < 2:
                result.log_messages.append("File has no data rows (only header or empty).")
                result.success = True
                result.original_row_count = max(len(all_rows) - 1, 0)
                result.cleaned_row_count = result.original_row_count
                result.quality_report = DataQualityReport(
                    completeness=100.0, duplicate_ratio=0.0, null_ratio=0.0,
                    total_cells=0, total_nulls=0, total_duplicates=0,
                )
                return result

            headers = all_rows[0]
            data_rows = all_rows[1:]
            result.original_row_count = len(data_rows)
            result.log_messages.append(f"Loaded {result.original_row_count} rows, {len(headers)} columns.")

            # Stage 1: Validation
            data_rows = self._validate_rows(data_rows, len(headers), result)

            # Stage 2: Cleaning — dedup + null handling
            data_rows = self._remove_duplicates(data_rows, result)
            data_rows = self._handle_nulls(data_rows, headers, result)

            # Stage 3: Normalization
            data_rows = self._normalize_strings(data_rows, result)

            result.cleaned_row_count = len(data_rows)

            # Stage 4: Statistics
            result.column_stats = self._compute_column_stats(headers, data_rows)
            result.quality_report = self._compute_quality_report(
                headers, data_rows, result
            )

            result.log_messages.append(
                f"Processing complete. {result.cleaned_row_count} clean rows."
            )

        except Exception as e:
            logger.exception("Processing pipeline failed")
            result.success = False
            result.error = str(e)
            result.log_messages.append(f"ERROR: {str(e)}")

        return result

    def process_json(self, content: bytes) -> ProcessingResult:
        """Process JSON file content (array of objects) through the pipeline."""
        result = ProcessingResult()
        try:
            text = content.decode("utf-8", errors="replace")
            data = json.loads(text)

            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list) or not data:
                result.log_messages.append("JSON is not an array of objects or is empty.")
                result.original_row_count = 0
                result.cleaned_row_count = 0
                result.quality_report = DataQualityReport(
                    completeness=100.0, duplicate_ratio=0.0, null_ratio=0.0,
                    total_cells=0, total_nulls=0, total_duplicates=0,
                )
                return result

            # Convert to tabular format (list of lists with headers)
            headers = list(data[0].keys()) if isinstance(data[0], dict) else []
            data_rows = []
            for record in data:
                if isinstance(record, dict):
                    data_rows.append([str(record.get(h, "")) for h in headers])

            result.original_row_count = len(data_rows)
            result.log_messages.append(f"Loaded {result.original_row_count} records, {len(headers)} fields.")

            # Run pipeline stages
            data_rows = self._remove_duplicates(data_rows, result)
            data_rows = self._handle_nulls(data_rows, headers, result)
            data_rows = self._normalize_strings(data_rows, result)

            result.cleaned_row_count = len(data_rows)
            result.column_stats = self._compute_column_stats(headers, data_rows)
            result.quality_report = self._compute_quality_report(headers, data_rows, result)
            result.log_messages.append(f"Processing complete. {result.cleaned_row_count} clean records.")

        except Exception as e:
            logger.exception("JSON processing failed")
            result.success = False
            result.error = str(e)
            result.log_messages.append(f"ERROR: {str(e)}")

        return result

    # ── Pipeline Stages ──

    def _validate_rows(
        self, rows: List[List[str]], expected_cols: int, result: ProcessingResult
    ) -> List[List[str]]:
        """Stage 1: Remove rows with incorrect column counts."""
        valid = []
        invalid_count = 0
        for row in rows:
            if len(row) == expected_cols:
                valid.append(row)
            else:
                invalid_count += 1
        if invalid_count > 0:
            result.log_messages.append(f"Validation: removed {invalid_count} malformed rows.")
        return valid

    def _remove_duplicates(
        self, rows: List[List[str]], result: ProcessingResult
    ) -> List[List[str]]:
        """Stage 2a: Remove exact duplicate rows."""
        seen = set()
        unique = []
        for row in rows:
            row_key = tuple(row)
            if row_key not in seen:
                seen.add(row_key)
                unique.append(row)
        removed = len(rows) - len(unique)
        result.duplicates_removed = removed
        if removed > 0:
            result.log_messages.append(f"Cleaning: removed {removed} duplicate rows.")
        return unique

    def _handle_nulls(
        self, rows: List[List[str]], headers: List[str], result: ProcessingResult
    ) -> List[List[str]]:
        """Stage 2b: Fill empty/null string values with 'N/A' placeholder."""
        fills = 0
        for row in rows:
            for i in range(len(row)):
                val = row[i].strip()
                if val == "" or val.lower() in ("null", "none", "nan", "n/a"):
                    row[i] = "N/A"
                    fills += 1
        result.nulls_filled = fills
        if fills > 0:
            result.log_messages.append(f"Cleaning: filled {fills} null/empty values with 'N/A'.")
        return rows

    def _normalize_strings(
        self, rows: List[List[str]], result: ProcessingResult
    ) -> List[List[str]]:
        """Stage 3: Trim whitespace and normalize string casing."""
        for row in rows:
            for i in range(len(row)):
                row[i] = row[i].strip()
        result.log_messages.append("Normalization: trimmed whitespace from all cells.")
        return rows

    def _compute_column_stats(
        self, headers: List[str], rows: List[List[str]]
    ) -> List[ColumnStats]:
        """Stage 4: Compute per-column statistics."""
        stats = []
        for col_idx, header in enumerate(headers):
            values = [row[col_idx] for row in rows if col_idx < len(row)]
            non_null = [v for v in values if v != "N/A"]
            null_count = len(values) - len(non_null)

            # Try to detect numeric columns
            numeric_vals = []
            for v in non_null:
                try:
                    numeric_vals.append(float(v))
                except (ValueError, TypeError):
                    pass

            is_numeric = len(numeric_vals) > len(non_null) * 0.5 and len(numeric_vals) > 0

            col_stat = ColumnStats(
                name=header,
                dtype="numeric" if is_numeric else "string",
                total_count=len(values),
                null_count=null_count,
                unique_count=len(set(non_null)),
                null_percentage=round((null_count / len(values) * 100) if values else 0, 2),
            )

            if is_numeric and numeric_vals:
                col_stat.min = round(min(numeric_vals), 4)
                col_stat.max = round(max(numeric_vals), 4)
                col_stat.mean = round(sum(numeric_vals) / len(numeric_vals), 4)
                if len(numeric_vals) > 1:
                    mean = col_stat.mean
                    variance = sum((x - mean) ** 2 for x in numeric_vals) / (len(numeric_vals) - 1)
                    col_stat.std = round(variance ** 0.5, 4)
            else:
                # Top 5 most frequent values for string columns
                from collections import Counter
                counter = Counter(non_null)
                col_stat.top_values = [val for val, _ in counter.most_common(5)]

            stats.append(col_stat)

        return stats

    def _compute_quality_report(
        self,
        headers: List[str],
        rows: List[List[str]],
        result: ProcessingResult,
    ) -> DataQualityReport:
        """Compute overall data quality metrics."""
        total_cells = len(rows) * len(headers) if headers else 0
        total_nulls = sum(
            1 for row in rows for val in row if val == "N/A"
        )

        completeness = ((total_cells - total_nulls) / total_cells * 100) if total_cells > 0 else 100.0
        null_ratio = (total_nulls / total_cells * 100) if total_cells > 0 else 0.0
        duplicate_ratio = (
            result.duplicates_removed / result.original_row_count * 100
        ) if result.original_row_count > 0 else 0.0

        return DataQualityReport(
            completeness=round(completeness, 2),
            duplicate_ratio=round(duplicate_ratio, 2),
            null_ratio=round(null_ratio, 2),
            total_cells=total_cells,
            total_nulls=total_nulls,
            total_duplicates=result.duplicates_removed,
        )


data_processor_service = DataProcessorService()
