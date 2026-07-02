<div align="center">

# 🧠 DecisionIQ AI

### Transforming Data into Intelligent Decisions

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Ready-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Gemini](https://img.shields.io/badge/Gemini_AI-Powered-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

**An enterprise-grade AI-powered Decision Intelligence Platform that enables organizations to upload structured and unstructured data, process it through intelligent pipelines, analyze with Google Gemini, generate business insights, predict trends, and deliver actionable recommendations through a multi-agent architecture.**

[Live Demo](#demo) · [Architecture](#high-level-system-architecture) · [Documentation](docs/) · [API Reference](docs/api.md) · [Deployment Guide](docs/deployment.md)

</div>

---

## 📋 Table of Contents

- [Executive Summary](#executive-summary)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [High-Level System Architecture](#high-level-system-architecture)
- [System Context Diagram](#system-context-diagram)
- [Component Architecture](#component-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Backend Architecture](#backend-architecture)
- [AI Multi-Agent Architecture](#ai-multi-agent-architecture)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Authentication Flow](#authentication-flow)
- [File Upload Flow](#file-upload-flow)
- [Database ER Diagram](#database-er-diagram)
- [Folder Structure](#folder-structure)
- [API Architecture](#api-architecture)
- [Security Architecture](#security-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Getting Started](#getting-started)
- [Business Value](#business-value)
- [Future Enhancements](#future-enhancements)

---

## Executive Summary

**DecisionIQ AI** is an enterprise-grade Decision Intelligence Platform designed to bridge the gap between raw data and actionable business decisions. Built on a modern, scalable architecture using **Google Cloud**, **Gemini AI**, **Google ADK (Agent Development Kit)**, **Model Context Protocol (MCP)**, and **Retrieval-Augmented Generation (RAG)**, the platform empowers business users, data analysts, and decision-makers with:

- **Automated Data Ingestion** — Upload CSV, Excel, PDF, JSON, TXT, and DOCX files with instant metadata extraction.
- **Intelligent Data Processing** — Four-stage pipeline performing validation, cleaning, normalization, and statistical profiling.
- **AI-Powered Insights** — Natural language conversations with Gemini to discover trends, anomalies, and recommendations.
- **Predictive Analytics** — Time-series forecasting and scenario modeling for forward-looking business planning.
- **Decision Engine** — Multi-agent orchestration that synthesizes data signals into ranked, confidence-scored recommendations.

The platform follows **Clean Architecture** principles, **Domain-Driven Design (DDD)**, and **SOLID** patterns with a clear separation of concerns across the API layer, service layer, repository pattern, and domain models.

---

## Problem Statement

Modern enterprises face critical challenges in data-driven decision making:

| Challenge | Impact |
|---|---|
| **Data Silos** | Business data scattered across CSV files, spreadsheets, PDFs, and databases |
| **Manual Analysis** | Analysts spend 60-80% of time cleaning and preparing data |
| **Insight Latency** | Weeks between data collection and actionable intelligence |
| **Decision Bottlenecks** | Key decisions delayed due to lack of synthesized, contextual information |
| **Tool Fragmentation** | Teams juggle multiple disconnected tools for analytics, reporting, and forecasting |

---

## Solution Overview

DecisionIQ AI addresses these challenges through a unified platform that automates the entire data-to-decision pipeline:

```mermaid
graph LR
    A["📂 Data Upload"] --> B["⚙️ Processing Pipeline"]
    B --> C["🧠 AI Analysis"]
    C --> D["📊 Insights & Predictions"]
    D --> E["✅ Intelligent Decisions"]

    style A fill:#1e293b,stroke:#8b5cf6,color:#e2e8f0
    style B fill:#1e293b,stroke:#6366f1,color:#e2e8f0
    style C fill:#1e293b,stroke:#8b5cf6,color:#e2e8f0
    style D fill:#1e293b,stroke:#6366f1,color:#e2e8f0
    style E fill:#1e293b,stroke:#10b981,color:#e2e8f0
```

**From raw data to intelligent decisions in minutes, not weeks.**

---

## Key Features

| Category | Features |
|---|---|
| 🔐 **Authentication** | Google OAuth 2.0, JWT tokens, Role-Based Access Control (Admin, Analyst, Business User, Auditor) |
| 📂 **Data Ingestion** | Multi-format upload (CSV, Excel, PDF, JSON, TXT, DOCX), drag-and-drop UI, metadata extraction |
| ⚙️ **Data Processing** | 4-stage pipeline: Validation → Cleaning → Normalization → Statistical Profiling |
| 🧠 **AI Chat** | Natural language queries powered by Google Gemini with context-aware responses |
| 📊 **Dashboard** | Real-time KPI cards, upload status tracking, AI insights panel, activity feed |
| 🔍 **RAG Search** | Retrieval-Augmented Generation for document-aware AI responses |
| 📈 **Predictive Analytics** | Trend analysis, anomaly detection, forecasting |
| 📝 **Report Generation** | Automated business intelligence reports |
| 🔔 **Notifications** | Real-time alerts for anomalies and processing completion |
| 🏗️ **Enterprise Architecture** | Clean Architecture, DDD, Repository Pattern, Service Layer, Dependency Injection |

---

## Technology Stack

### Backend
| Technology | Purpose | Version |
|---|---|---|
| **Python** | Core runtime | 3.12+ |
| **FastAPI** | API framework | 0.111 |
| **SQLAlchemy** | ORM / database | 2.0 |
| **Pydantic** | Validation & schemas | 2.7 |
| **Alembic** | Database migrations | 1.13 |
| **PyJWT** | JWT token management | 2.8 |
| **Bcrypt** | Password hashing | Native |
| **Pandas** | Data manipulation | 2.2 |
| **PyPDF2** | PDF processing | 3.0 |
| **python-docx** | DOCX processing | 1.1 |
| **openpyxl** | Excel processing | 3.1 |

### Frontend
| Technology | Purpose | Version |
|---|---|---|
| **Next.js** | React framework | 16 (App Router) |
| **React** | UI library | 19 |
| **TypeScript** | Type safety | 5.x |
| **Tailwind CSS** | Utility-first styling | 4.x |
| **TanStack Query** | Server state management | 5.x |

### Google Cloud Services (Production-Ready)
| Service | Purpose |
|---|---|
| **Cloud Run** | Containerized backend deployment |
| **Cloud SQL** | Managed PostgreSQL |
| **Cloud Storage (GCS)** | File storage for uploaded datasets |
| **BigQuery** | Large-scale analytics warehouse |
| **Vertex AI** | Gemini model hosting |
| **Secret Manager** | Credential and key management |
| **Cloud Build** | CI/CD pipeline |
| **Cloud Monitoring** | Observability and alerting |

### AI & Intelligence
| Technology | Purpose |
|---|---|
| **Google Gemini** | LLM for natural language insights |
| **Google ADK** | Multi-agent orchestration framework |
| **MCP (Model Context Protocol)** | Standardized tool-model communication |
| **RAG** | Context-augmented retrieval for grounded responses |

---

## High-Level System Architecture

```mermaid
graph TB
    subgraph Client["Client Layer"]
        WEB["🖥️ Next.js Frontend<br/>React 19 + TypeScript"]
        MOBILE["📱 Mobile Client<br/>(Future)"]
    end

    subgraph Gateway["API Gateway Layer"]
        API["⚡ FastAPI Backend<br/>REST API v1"]
        AUTH["🔐 Auth Middleware<br/>JWT + OAuth 2.0"]
    end

    subgraph Services["Service Layer"]
        FP["📄 File Processor<br/>Multi-format Parser"]
        DP["⚙️ Data Processor<br/>4-Stage Pipeline"]
        SS["💾 Storage Service<br/>Local / GCS"]
    end

    subgraph AI["AI Intelligence Layer"]
        GEMINI["🧠 Google Gemini<br/>LLM Engine"]
        ADK["🤖 Google ADK<br/>Agent Orchestration"]
        RAG["🔍 RAG Engine<br/>Context Retrieval"]
        MCP["🔌 MCP Server<br/>Tool Protocol"]
    end

    subgraph Data["Data Layer"]
        PG["🐘 PostgreSQL<br/>Relational Data"]
        BQ["📊 BigQuery<br/>Analytics Warehouse"]
        GCS["☁️ Cloud Storage<br/>File Storage"]
        VS["🧲 Vector Store<br/>Embeddings"]
    end

    WEB --> API
    MOBILE -.-> API
    API --> AUTH
    AUTH --> FP
    AUTH --> DP
    AUTH --> SS
    AUTH --> ADK
    FP --> SS
    DP --> PG
    SS --> GCS
    ADK --> GEMINI
    ADK --> RAG
    ADK --> MCP
    RAG --> VS
    MCP --> BQ
    MCP --> PG

    style Client fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Gateway fill:#0f172a,stroke:#6366f1,color:#e2e8f0
    style Services fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style AI fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Data fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** The platform follows a layered architecture with clear separation between presentation, API gateway, business services, AI intelligence, and data persistence. Each layer communicates through well-defined interfaces, enabling independent scaling and technology evolution.

---

## System Context Diagram

```mermaid
graph TB
    USER["👤 Business User<br/>Analyst / Decision Maker"]
    ADMIN["👤 Platform Admin"]

    SYSTEM["🧠 DecisionIQ AI Platform"]

    GOOGLE["🔐 Google OAuth<br/>Identity Provider"]
    GEMINI_API["🧠 Google Gemini API<br/>AI/ML Service"]
    GCS_EXT["☁️ Google Cloud Storage<br/>File Persistence"]
    PGDB["🐘 PostgreSQL<br/>Application Database"]
    BQ_EXT["📊 BigQuery<br/>Analytics Engine"]
    SMTP["📧 Email Service<br/>Notifications"]

    USER -->|"Upload data, query AI, view insights"| SYSTEM
    ADMIN -->|"Manage users, configure platform"| SYSTEM
    SYSTEM -->|"Authenticate users"| GOOGLE
    SYSTEM -->|"Generate insights & predictions"| GEMINI_API
    SYSTEM -->|"Store uploaded files"| GCS_EXT
    SYSTEM -->|"Persist application data"| PGDB
    SYSTEM -->|"Run analytics queries"| BQ_EXT
    SYSTEM -->|"Send alerts"| SMTP

    style SYSTEM fill:#1e1b4b,stroke:#8b5cf6,color:#e2e8f0
    style USER fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style ADMIN fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
```

**Explanation:** The System Context Diagram (C4 Level 1) shows DecisionIQ AI as the central system, with its primary actors (Business Users and Admins) and external dependencies (Google services, database, email). This view communicates the platform's integration boundaries to stakeholders.

---

## Component Architecture

```mermaid
graph TB
    subgraph Frontend["Frontend Application"]
        LOGIN["Login Page"]
        DASH["Dashboard Page"]
        UPLOAD["Upload Page"]
        CHAT["AI Chat Page"]
        ANALYTICS["Analytics Page"]
        REPORTS["Reports Page"]
    end

    subgraph API_Layer["API Layer - FastAPI Routers"]
        R_AUTH["/api/v1/auth"]
        R_DASH["/api/v1/dashboard"]
        R_UPLOAD["/api/v1/upload"]
        R_PROC["/api/v1/processing"]
    end

    subgraph Service_Layer["Service Layer"]
        SVC_FILE["FileProcessorService"]
        SVC_DATA["DataProcessorService"]
        SVC_STORE["StorageService"]
    end

    subgraph Repository_Layer["Repository / CRUD Layer"]
        REPO_USER["UserRepository"]
        REPO_DS["DatasetRepository"]
        REPO_DASH["DashboardRepository"]
    end

    subgraph Domain_Models["Domain Models"]
        M_USER["User"]
        M_DS["Dataset"]
        M_INSIGHT["AIInsight"]
        M_ACTIVITY["ActivityLog"]
        M_REPORT["ProcessingReport"]
    end

    LOGIN --> R_AUTH
    DASH --> R_DASH
    UPLOAD --> R_UPLOAD
    UPLOAD --> R_PROC
    CHAT -.-> R_AUTH

    R_AUTH --> REPO_USER
    R_DASH --> REPO_DASH
    R_UPLOAD --> SVC_FILE
    R_UPLOAD --> SVC_STORE
    R_PROC --> SVC_DATA

    SVC_FILE --> REPO_DS
    SVC_DATA --> REPO_DS
    SVC_STORE --> REPO_DS

    REPO_USER --> M_USER
    REPO_DS --> M_DS
    REPO_DASH --> M_INSIGHT
    REPO_DASH --> M_ACTIVITY
    REPO_DASH --> M_DS

    style Frontend fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style API_Layer fill:#0f172a,stroke:#6366f1,color:#e2e8f0
    style Service_Layer fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Repository_Layer fill:#0f172a,stroke:#0ea5e9,color:#e2e8f0
    style Domain_Models fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** The Component Architecture illustrates the Clean Architecture layers. Frontend pages communicate exclusively through versioned API routes. Each route delegates to service classes for business logic, which in turn use repository classes for data access. Domain models are pure data structures with no framework dependencies.

---

## Frontend Architecture

```mermaid
graph TB
    subgraph App_Shell["Application Shell"]
        LAYOUT["RootLayout<br/>Providers + Font + Metadata"]
        PROVIDERS["Providers<br/>QueryClient + AuthProvider"]
    end

    subgraph Auth_Layer["Auth Layer"]
        AUTH_CTX["AuthContext<br/>useAuth Hook"]
        AUTH_GUARD["AppShell<br/>Route Protection"]
    end

    subgraph Pages["Page Components"]
        P_LOGIN["LoginPage<br/>/login"]
        P_DASH["DashboardPage<br/>/dashboard"]
        P_UPLOAD["UploadPage<br/>/upload"]
    end

    subgraph Shared["Shared Components"]
        SIDEBAR["Sidebar<br/>Collapsible Nav"]
        HEADER["Header<br/>User Profile Menu"]
        KPI["KpiCard<br/>Animated Metrics"]
        BADGE["StatusBadge<br/>Color-coded States"]
        DROPZONE["FileDropzone<br/>Drag-and-Drop"]
    end

    subgraph Data_Layer["Data Fetching Layer"]
        API_CLIENT["ApiClient<br/>JWT Interceptor"]
        TQ["TanStack Query<br/>Cache + Mutations"]
    end

    LAYOUT --> PROVIDERS
    PROVIDERS --> AUTH_CTX
    AUTH_CTX --> AUTH_GUARD
    AUTH_GUARD --> P_DASH
    AUTH_GUARD --> P_UPLOAD
    P_LOGIN --> AUTH_CTX

    P_DASH --> SIDEBAR
    P_DASH --> HEADER
    P_DASH --> KPI
    P_DASH --> BADGE

    P_UPLOAD --> DROPZONE
    P_UPLOAD --> BADGE

    P_DASH --> TQ
    P_UPLOAD --> TQ
    TQ --> API_CLIENT

    style App_Shell fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Auth_Layer fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
    style Pages fill:#0f172a,stroke:#6366f1,color:#e2e8f0
    style Shared fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Data_Layer fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** The frontend follows Next.js 16 App Router patterns. The `RootLayout` wraps all pages in `QueryProvider` and `AuthProvider`. The `AppShell` component acts as an authentication guard — redirecting unauthenticated users to `/login`. All API calls flow through a centralized `ApiClient` with automatic JWT token injection.

---

## Backend Architecture

```mermaid
graph TB
    subgraph Entrypoint["Application Entrypoint"]
        MAIN["main.py<br/>FastAPI App + Lifespan"]
        CORS["CORS Middleware"]
        EXC["Exception Handlers"]
    end

    subgraph Routers["API Routers"]
        R1["auth.py<br/>POST /register, /login, /google-login<br/>GET /me"]
        R2["dashboard.py<br/>GET /dashboard"]
        R3["upload.py<br/>POST /upload<br/>GET /upload, /upload/:id"]
        R4["processing.py<br/>POST /processing/:id<br/>GET /processing/:id/report"]
    end

    subgraph Dependencies["Dependency Injection"]
        DEP_DB["get_db<br/>Session Factory"]
        DEP_USER["get_current_user<br/>JWT Decoder"]
    end

    subgraph Core["Core Infrastructure"]
        CONFIG["Settings<br/>Pydantic BaseSettings"]
        DB["Database Engine<br/>SQLAlchemy 2.0"]
        SEC["Security<br/>JWT + Bcrypt"]
    end

    MAIN --> CORS
    MAIN --> EXC
    MAIN --> R1
    MAIN --> R2
    MAIN --> R3
    MAIN --> R4

    R1 --> DEP_DB
    R1 --> DEP_USER
    R2 --> DEP_DB
    R2 --> DEP_USER
    R3 --> DEP_DB
    R3 --> DEP_USER
    R4 --> DEP_DB
    R4 --> DEP_USER

    DEP_DB --> DB
    DEP_USER --> SEC
    DB --> CONFIG

    style Entrypoint fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Routers fill:#0f172a,stroke:#6366f1,color:#e2e8f0
    style Dependencies fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Core fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** The backend uses FastAPI's dependency injection system. Every router receives database sessions and authenticated user context through `Depends()`. Core infrastructure (config, database, security) is initialized once at startup and shared across all request handlers.

---

## AI Multi-Agent Architecture

```mermaid
graph TB
    subgraph Orchestrator["🤖 Orchestrator Agent"]
        ORC["Agent Router<br/>Intent Classification"]
    end

    subgraph Agents["Specialized Agents"]
        A1["📊 Analytics Agent<br/>Statistical Analysis"]
        A2["📈 Forecast Agent<br/>Trend Prediction"]
        A3["🔍 Research Agent<br/>RAG + Semantic Search"]
        A4["📝 Report Agent<br/>Document Generation"]
        A5["⚠️ Anomaly Agent<br/>Outlier Detection"]
        A6["✅ Decision Agent<br/>Recommendation Engine"]
    end

    subgraph Tools["MCP Tool Registry"]
        T1["query_dataset"]
        T2["compute_statistics"]
        T3["search_embeddings"]
        T4["generate_forecast"]
        T5["create_report"]
    end

    subgraph Models["AI Models"]
        GEMINI_M["Google Gemini 2.0<br/>Foundation Model"]
    end

    ORC -->|"Data question"| A1
    ORC -->|"Future prediction"| A2
    ORC -->|"Document search"| A3
    ORC -->|"Generate report"| A4
    ORC -->|"Find anomalies"| A5
    ORC -->|"Recommend action"| A6

    A1 --> T1
    A1 --> T2
    A2 --> T4
    A3 --> T3
    A4 --> T5
    A5 --> T1
    A6 --> T2

    A1 --> GEMINI_M
    A2 --> GEMINI_M
    A3 --> GEMINI_M
    A4 --> GEMINI_M
    A5 --> GEMINI_M
    A6 --> GEMINI_M

    style Orchestrator fill:#1e1b4b,stroke:#8b5cf6,color:#e2e8f0
    style Agents fill:#0f172a,stroke:#6366f1,color:#e2e8f0
    style Tools fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Models fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
```

**Explanation:** The multi-agent architecture uses Google ADK to orchestrate six specialized AI agents. The Orchestrator Agent classifies user intent and delegates to the appropriate specialist. Each agent has access to MCP-registered tools for data retrieval, computation, and generation. All agents share the Gemini 2.0 foundation model for reasoning.

---

## Data Processing Pipeline

```mermaid
graph LR
    subgraph Input["📂 Input"]
        RAW["Raw File<br/>CSV / JSON / Excel"]
    end

    subgraph Stage1["Stage 1: Validation"]
        V1["Column Count Check"]
        V2["Structure Integrity"]
        V3["Malformed Row Removal"]
    end

    subgraph Stage2["Stage 2: Cleaning"]
        C1["Duplicate Detection"]
        C2["Null/NaN Handling"]
        C3["Empty Value Filling"]
    end

    subgraph Stage3["Stage 3: Normalization"]
        N1["Whitespace Trimming"]
        N2["String Standardization"]
        N3["Date Format Unification"]
    end

    subgraph Stage4["Stage 4: Profiling"]
        P1["Type Classification<br/>Numeric vs String"]
        P2["Column Statistics<br/>min/max/mean/std"]
        P3["Quality Report<br/>Completeness/Nulls/Duplicates"]
    end

    subgraph Output["📊 Output"]
        REPORT["ProcessingReport<br/>JSON Persisted"]
        STATUS["Dataset Status<br/>→ completed"]
    end

    RAW --> V1 --> V2 --> V3
    V3 --> C1 --> C2 --> C3
    C3 --> N1 --> N2 --> N3
    N3 --> P1 --> P2 --> P3
    P3 --> REPORT
    P3 --> STATUS

    style Input fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Stage1 fill:#0f172a,stroke:#ef4444,color:#e2e8f0
    style Stage2 fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
    style Stage3 fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Stage4 fill:#0f172a,stroke:#10b981,color:#e2e8f0
    style Output fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
```

**Explanation:** Every uploaded structured dataset passes through this four-stage pipeline. Stage 1 validates structural integrity. Stage 2 removes exact duplicates and fills null values with `N/A` placeholders. Stage 3 normalizes string formatting. Stage 4 computes per-column statistics and generates a comprehensive data quality report persisted as JSON in the `ProcessingReport` table.

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Next.js Frontend
    participant API as FastAPI Backend
    participant G as Google OAuth
    participant DB as PostgreSQL

    Note over U, DB: Email/Password Login Flow
    U->>FE: Enter credentials
    FE->>API: POST /api/v1/auth/login
    API->>DB: Verify user + bcrypt hash
    DB-->>API: User record
    API->>API: Generate JWT (HS256)
    API-->>FE: {access_token, token_type}
    FE->>FE: Store token in localStorage
    FE->>API: GET /api/v1/auth/me (Bearer token)
    API-->>FE: User profile

    Note over U, DB: Google OAuth Flow
    U->>FE: Click "Sign in with Google"
    FE->>G: Redirect to Google consent
    G-->>FE: ID Token
    FE->>API: POST /api/v1/auth/google-login
    API->>G: Verify ID token
    G-->>API: User info (email, name)
    API->>DB: Find or create user
    API->>API: Generate JWT
    API-->>FE: {access_token}
```

**Explanation:** The platform supports dual authentication flows. Email/password login uses bcrypt for password hashing and returns a JWT token valid for 8 days. Google OAuth verifies ID tokens server-side and auto-provisions user accounts on first login. All authenticated API calls require a `Bearer` token in the `Authorization` header.

---

## File Upload Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Upload Router
    participant FPS as FileProcessorService
    participant SS as StorageService
    participant DR as DatasetRepository
    participant LOG as ActivityLog

    U->>FE: Drop file on Dropzone
    FE->>API: POST /api/v1/upload (multipart)
    API->>FPS: validate_file(file)
    FPS->>FPS: Check extension + size
    FPS-->>API: Validation passed

    API->>FPS: extract_metadata(file)
    FPS->>FPS: Parse format-specific metadata
    FPS-->>API: FileMetadata (rows, columns, pages)

    API->>SS: save_file(file, user_dir)
    SS->>SS: UUID-prefix filename
    SS-->>API: storage_uri

    API->>DR: create(name, type, size, user_id)
    DR->>DR: Insert Dataset record
    DR-->>API: Dataset object

    API->>LOG: log_activity(user, "file_upload")
    API-->>FE: UploadResponse (dataset + metadata)
    FE->>FE: Display metadata cards
    FE->>FE: Refresh dataset table
```

**Explanation:** The file upload flow orchestrates five discrete operations: validation (type + size), metadata extraction (format-specific parsing), storage (UUID-prefixed local/GCS persistence), database persistence (Dataset record creation), and audit logging. The frontend receives both the created dataset record and extracted metadata for immediate display.

---

## Database ER Diagram

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string hashed_password
        string full_name
        enum role
        boolean is_active
        string avatar_url
        string google_id
        datetime created_at
        datetime updated_at
    }

    DATASET {
        int id PK
        string name
        string file_type
        int file_size
        enum status
        int row_count
        string gcs_uri
        string bq_table_id
        int user_id FK
        datetime created_at
        datetime updated_at
    }

    AI_INSIGHT {
        int id PK
        string title
        text content
        enum insight_type
        float confidence_score
        int dataset_id FK
        int user_id FK
        datetime created_at
    }

    ACTIVITY_LOG {
        int id PK
        int user_id FK
        string action
        text details
        datetime created_at
    }

    PROCESSING_REPORT {
        int id PK
        int dataset_id FK UK
        json quality_report
        json column_stats
        int original_row_count
        int cleaned_row_count
        int duplicates_removed
        int nulls_filled
        text log
        datetime created_at
    }

    USER ||--o{ DATASET : "uploads"
    USER ||--o{ AI_INSIGHT : "receives"
    USER ||--o{ ACTIVITY_LOG : "generates"
    DATASET ||--o{ AI_INSIGHT : "produces"
    DATASET ||--o| PROCESSING_REPORT : "has"
```

**Explanation:** The database schema centers on five core entities. `User` owns datasets and generates activity. `Dataset` tracks uploaded files through their lifecycle (pending → processing → completed/failed). `ProcessingReport` stores quality metrics and column statistics as JSON for flexible schema evolution. `AIInsight` captures generated business intelligence with confidence scores. `ActivityLog` provides a complete audit trail.

---

## Folder Structure

```
DecisionIQ AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py                 # Dependency injection (DB, Auth)
│   │   │   └── v1/
│   │   │       ├── auth.py             # Authentication endpoints
│   │   │       ├── dashboard.py        # Dashboard KPI endpoint
│   │   │       ├── upload.py           # File upload endpoints
│   │   │       └── processing.py       # Data processing endpoints
│   │   ├── core/
│   │   │   ├── config.py              # Application settings
│   │   │   ├── database.py            # SQLAlchemy engine & session
│   │   │   ├── exceptions.py          # Custom exception classes
│   │   │   └── security.py            # JWT & bcrypt utilities
│   │   ├── crud/
│   │   │   ├── user.py                # User CRUD repository
│   │   │   ├── dataset.py             # Dataset CRUD repository
│   │   │   └── dashboard.py           # Dashboard aggregation queries
│   │   ├── models/
│   │   │   ├── user.py                # User SQLAlchemy model
│   │   │   ├── dataset.py             # Dataset model + DatasetStatus enum
│   │   │   ├── insight.py             # AIInsight model
│   │   │   ├── activity.py            # ActivityLog model
│   │   │   └── processing_report.py   # ProcessingReport model
│   │   ├── schemas/
│   │   │   ├── user.py                # User Pydantic schemas
│   │   │   ├── dataset.py             # Dataset/Upload schemas
│   │   │   ├── dashboard.py           # Dashboard response schemas
│   │   │   └── processing.py          # Processing result schemas
│   │   ├── services/
│   │   │   ├── storage.py             # Storage abstraction (Local/GCS)
│   │   │   ├── file_processor.py      # File validation & metadata extraction
│   │   │   └── data_processor.py      # 4-stage processing pipeline
│   │   └── main.py                    # FastAPI application entrypoint
│   ├── tests/
│   │   ├── conftest.py                # Test fixtures (DB, client)
│   │   ├── test_auth.py               # Authentication tests (7)
│   │   ├── test_dashboard.py          # Dashboard tests (3)
│   │   ├── test_upload.py             # Upload tests (9)
│   │   └── test_processing.py         # Processing tests (6)
│   └── requirements.txt               # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx             # Root layout + providers
│   │   │   ├── providers.tsx          # QueryClient + Auth wrapper
│   │   │   ├── page.tsx               # Root redirect → /dashboard
│   │   │   ├── login/page.tsx         # Login page (glassmorphism)
│   │   │   ├── dashboard/page.tsx     # Dashboard page (KPIs, tables)
│   │   │   └── upload/page.tsx        # Upload page (dropzone, table)
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── sidebar.tsx        # Collapsible navigation
│   │   │   │   ├── header.tsx         # User profile header
│   │   │   │   └── app-shell.tsx      # Authenticated shell
│   │   │   ├── kpi-card.tsx           # KPI metric card
│   │   │   ├── status-badge.tsx       # Color-coded badges
│   │   │   └── file-dropzone.tsx      # Drag-and-drop upload zone
│   │   └── lib/
│   │       ├── api.ts                 # Centralized API client
│   │       ├── auth.tsx               # Auth context + useAuth hook
│   │       ├── query-provider.tsx     # TanStack Query provider
│   │       └── utils.ts              # Utility functions
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
└── docs/                              # Enterprise documentation
    ├── README.md
    ├── architecture.md
    └── ...
```

---

## API Architecture

```mermaid
graph LR
    subgraph Auth["🔐 Authentication API"]
        A1["POST /auth/register"]
        A2["POST /auth/login"]
        A3["POST /auth/google-login"]
        A4["GET /auth/me"]
    end

    subgraph Dashboard["📊 Dashboard API"]
        D1["GET /dashboard"]
    end

    subgraph Upload["📂 Upload API"]
        U1["POST /upload"]
        U2["GET /upload"]
        U3["GET /upload/:id"]
    end

    subgraph Processing["⚙️ Processing API"]
        P1["POST /processing/:id"]
        P2["GET /processing/:id/report"]
    end

    CLIENT["Client"] --> A1
    CLIENT --> A2
    CLIENT --> A3
    CLIENT --> A4
    CLIENT --> D1
    CLIENT --> U1
    CLIENT --> U2
    CLIENT --> U3
    CLIENT --> P1
    CLIENT --> P2

    style Auth fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
    style Dashboard fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Upload fill:#0f172a,stroke:#3b82f6,color:#e2e8f0
    style Processing fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/v1/auth/register` | POST | ❌ | Register new user |
| `/api/v1/auth/login` | POST | ❌ | Login with email/password |
| `/api/v1/auth/google-login` | POST | ❌ | Login with Google OAuth |
| `/api/v1/auth/me` | GET | ✅ | Get current user profile |
| `/api/v1/dashboard` | GET | ✅ | Dashboard KPIs, uploads, insights, activity |
| `/api/v1/upload` | POST | ✅ | Upload file (multipart) |
| `/api/v1/upload` | GET | ✅ | List user's datasets |
| `/api/v1/upload/:id` | GET | ✅ | Get dataset by ID |
| `/api/v1/processing/:id` | POST | ✅ | Trigger processing pipeline |
| `/api/v1/processing/:id/report` | GET | ✅ | Get processing report |

---

## Security Architecture

```mermaid
graph TB
    subgraph Perimeter["Network Perimeter"]
        LB["🌐 Load Balancer<br/>HTTPS Termination"]
        WAF["🛡️ WAF<br/>Rate Limiting"]
    end

    subgraph Auth_Security["Authentication Layer"]
        OAUTH["Google OAuth 2.0<br/>Identity Verification"]
        JWT_V["JWT Validation<br/>HS256 Signing"]
        BCRYPT["Bcrypt Hashing<br/>Password Storage"]
    end

    subgraph RBAC["Role-Based Access Control"]
        ADMIN_R["Admin<br/>Full Access"]
        ANALYST_R["Analyst<br/>Data + AI Access"]
        BIZ_R["Business User<br/>Dashboard + Upload"]
        AUDIT_R["Auditor<br/>Read-Only Access"]
    end

    subgraph Data_Security["Data Security"]
        ENCRYPT["AES-256 Encryption<br/>Data at Rest"]
        TLS["TLS 1.3<br/>Data in Transit"]
        SECRETS["Secret Manager<br/>Credential Storage"]
    end

    LB --> WAF
    WAF --> OAUTH
    WAF --> JWT_V
    OAUTH --> RBAC
    JWT_V --> RBAC
    JWT_V --> BCRYPT
    RBAC --> Data_Security

    style Perimeter fill:#0f172a,stroke:#ef4444,color:#e2e8f0
    style Auth_Security fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
    style RBAC fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Data_Security fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** Security is implemented at multiple layers. Network perimeter with HTTPS and rate limiting. Authentication via Google OAuth and JWT with bcrypt password hashing. Authorization via four RBAC roles with granular permissions. Data protection with encryption at rest and TLS in transit.

---

## Deployment Architecture

```mermaid
graph TB
    subgraph CI_CD["CI/CD Pipeline"]
        GH["GitHub Repository"]
        CB["Cloud Build<br/>Docker Build + Test"]
        AR["Artifact Registry<br/>Container Images"]
    end

    subgraph Production["Production Environment"]
        CR_FE["Cloud Run<br/>Frontend Container"]
        CR_BE["Cloud Run<br/>Backend Container"]
        CSQL["Cloud SQL<br/>PostgreSQL 15"]
        GCS_D["Cloud Storage<br/>Dataset Files"]
        SM["Secret Manager<br/>API Keys + Secrets"]
    end

    subgraph Monitoring_D["Observability"]
        CM["Cloud Monitoring<br/>Metrics + Dashboards"]
        CL["Cloud Logging<br/>Structured Logs"]
        CT["Cloud Trace<br/>Distributed Tracing"]
    end

    GH -->|"Push to main"| CB
    CB -->|"Build images"| AR
    AR -->|"Deploy"| CR_FE
    AR -->|"Deploy"| CR_BE
    CR_BE --> CSQL
    CR_BE --> GCS_D
    CR_BE --> SM
    CR_BE --> CM
    CR_BE --> CL
    CR_BE --> CT

    style CI_CD fill:#0f172a,stroke:#f59e0b,color:#e2e8f0
    style Production fill:#0f172a,stroke:#8b5cf6,color:#e2e8f0
    style Monitoring_D fill:#0f172a,stroke:#10b981,color:#e2e8f0
```

**Explanation:** Production deployment uses Cloud Run for auto-scaling container hosting. Cloud Build runs CI/CD on every push to main — building Docker images, running tests, and deploying to Cloud Run. Cloud SQL provides managed PostgreSQL. Cloud Storage handles file persistence. Secret Manager secures all credentials.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/decisioniq-ai.git
cd decisioniq-ai

# Backend Setup
python -m venv .venv
.venv/Scripts/activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r backend/requirements.txt

# Start Backend API
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# Frontend Setup (new terminal)
cd frontend
npm install
npm run dev
```

### Access Points

| Service | URL |
|---|---|
| Frontend Application | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |

### Running Tests

```bash
# Run all 25 integration tests
python -m pytest backend/tests -v

# Run with coverage
python -m pytest backend/tests --cov=backend/app
```

---

## Business Value

| Metric | Before DecisionIQ | After DecisionIQ |
|---|---|---|
| **Data Preparation Time** | 4-6 hours per dataset | Under 2 minutes (automated) |
| **Insight Generation** | 2-3 weeks | Real-time |
| **Decision Latency** | Days to weeks | Minutes |
| **Tool Consolidation** | 5-7 separate tools | Single unified platform |
| **Data Quality Assurance** | Manual spot-checks | Automated quality reports |
| **Audit Compliance** | Fragmented logs | Complete activity audit trail |

---

## Future Enhancements

| Phase | Enhancement | Description |
|---|---|---|
| Phase 2 | **AI Chat Module** | Natural language querying with Gemini integration |
| Phase 2 | **RAG Engine** | Embedding generation + vector search for document-aware AI |
| Phase 3 | **Predictive Analytics** | Time-series forecasting and scenario modeling |
| Phase 3 | **Decision Engine** | Multi-signal synthesis with confidence-scored recommendations |
| Phase 4 | **Report Generation** | Automated business intelligence report creation |
| Phase 4 | **Real-time Alerts** | Anomaly detection with push notifications |
| Phase 5 | **Mobile Application** | Cross-platform mobile client |
| Phase 5 | **Multi-tenant Architecture** | Organization-level isolation and billing |

---

## Testing Strategy

| Test Type | Count | Framework | Description |
|---|---|---|---|
| **Authentication** | 7 | pytest | Registration, login, JWT, RBAC, Google OAuth |
| **Dashboard** | 3 | pytest | Auth guard, empty state, aggregated data |
| **File Upload** | 9 | pytest | Multi-format upload, validation, listing, retrieval |
| **Data Processing** | 6 | pytest | CSV/JSON processing, stats, unsupported types, reports |
| **Total** | **25** | pytest | All passing ✅ |

---

## Architecture Decision Records (ADR)

| ADR | Decision | Rationale |
|---|---|---|
| ADR-001 | Native bcrypt over passlib | passlib has deprecation warnings on Python 3.12+; native bcrypt is actively maintained |
| ADR-002 | SQLite for development | Zero-config local development; production uses Cloud SQL PostgreSQL |
| ADR-003 | StorageService abstraction | Decouple file persistence from cloud provider; swap Local→GCS without code changes |
| ADR-004 | JSON columns for reports | Processing reports have variable schemas per file type; JSON provides flexible evolution |
| ADR-005 | Deterministic sort: `created_at.desc(), id.desc()` | Bulk inserts can have identical timestamps; secondary ID sort ensures stable ordering |
| ADR-006 | TanStack Query over SWR | Superior mutation support, query invalidation, and DevTools for complex data flows |

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using Google Cloud, Gemini AI, and Modern Web Technologies**

[⬆ Back to Top](#-decisioniq-ai)

</div>
