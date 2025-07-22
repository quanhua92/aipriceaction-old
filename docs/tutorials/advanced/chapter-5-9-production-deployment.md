# Chương 5.9: Production Deployment
## Triển Khai Hệ Thống VPA Lên Cloud

### 🎯 Mục Tiêu Chương

Bạn đã xây dựng được hệ thống VPA hoàn chỉnh. Bây giờ là lúc đưa nó lên production để hoạt động 24/7 tự động, từ thu thập dữ liệu đến gửi alerts và quản lý portfolio.

### 💡 Tầm Nhìn Production

**"Từ prototype thành hệ thống chuyên nghiệp"**

- ☁️ **Cloud Infrastructure** - AWS/GCP/Azure với auto-scaling
- 🔄 **CI/CD Pipeline** - Deploy tự động, zero-downtime
- 📊 **Monitoring & Logging** - Theo dõi health system 24/7
- 🔒 **Security & Backup** - Bảo mật dữ liệu và disaster recovery
- 📱 **API Gateway** - Interface cho mobile app/web dashboard

---

## 📚 Phần 1: Cơ Bản - Containerization & Orchestration

### A. Cấu Hình Docker

```dockerfile
# Dockerfile cho VPA System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create non-root user
RUN useradd -m -u 1000 vpauser && chown -R vpauser:vpauser /app
USER vpauser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "src/main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  vpa-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/vpa_db
      - REDIS_URL=redis://redis:6379
      - ENV=production
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    
  vpa-scanner:
    build: .
    command: python src/market_scanner.py
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/vpa_db
      - REDIS_URL=redis://redis:6379
      - SCAN_INTERVAL=300  # 5 minutes
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  vpa-alerts:
    build: .
    command: python src/alert_system.py
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/vpa_db
      - REDIS_URL=redis://redis:6379
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=vpa_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
      
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - vpa-api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### B. Lược Đồ Cơ Sở Dữ Liệu

```sql
-- init.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Stocks master table
CREATE TABLE stocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    sector VARCHAR(100),
    market VARCHAR(20) DEFAULT 'HOSE',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market data table
CREATE TABLE market_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id),
    date DATE NOT NULL,
    open_price DECIMAL(12,2),
    high_price DECIMAL(12,2),
    low_price DECIMAL(12,2),
    close_price DECIMAL(12,2),
    volume BIGINT,
    value BIGINT,
    foreign_buy BIGINT DEFAULT 0,
    foreign_sell BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date)
);

-- VPA signals table
CREATE TABLE vpa_signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id),
    signal_date DATE NOT NULL,
    signal_type VARCHAR(50) NOT NULL,
    vpa_score INTEGER CHECK (vpa_score >= 0 AND vpa_score <= 100),
    confidence_score DECIMAL(4,3) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    volume_ratio DECIMAL(6,2),
    price_change DECIMAL(6,4),
    conditions JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vpa_signal_id UUID REFERENCES vpa_signals(id),
    alert_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    message TEXT NOT NULL,
    channels_sent TEXT[],
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_sent BOOLEAN DEFAULT FALSE
);

-- Portfolio positions table
CREATE TABLE portfolio_positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID REFERENCES stocks(id),
    entry_date DATE NOT NULL,
    entry_price DECIMAL(12,2) NOT NULL,
    shares INTEGER NOT NULL,
    position_value DECIMAL(15,2) NOT NULL,
    stop_loss DECIMAL(12,2),
    take_profit DECIMAL(12,2),
    vpa_signal_id UUID REFERENCES vpa_signals(id),
    exit_date DATE,
    exit_price DECIMAL(12,2),
    realized_pnl DECIMAL(15,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance tracking table
CREATE TABLE portfolio_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL UNIQUE,
    total_value DECIMAL(15,2) NOT NULL,
    cash_value DECIMAL(15,2) NOT NULL,
    invested_value DECIMAL(15,2) NOT NULL,
    daily_return DECIMAL(8,6),
    cumulative_return DECIMAL(8,6),
    benchmark_return DECIMAL(8,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_market_data_stock_date ON market_data(stock_id, date DESC);
CREATE INDEX idx_vpa_signals_stock_date ON vpa_signals(stock_id, signal_date DESC);
CREATE INDEX idx_vpa_signals_type_score ON vpa_signals(signal_type, vpa_score DESC);
CREATE INDEX idx_portfolio_positions_active ON portfolio_positions(is_active, entry_date DESC);
CREATE INDEX idx_alerts_sent ON alerts(is_sent, sent_at DESC);

-- Insert initial stock data
INSERT INTO stocks (symbol, name, sector) VALUES
('VCB', 'Ngân hàng Ngoại thương Việt Nam', 'Banking'),
('TCB', 'Ngân hàng Kỹ thương Việt Nam', 'Banking'),
('BID', 'Ngân hàng Đầu tư Phát triển', 'Banking'),
('HPG', 'Tập đoàn Hoa Phát', 'Steel'),
('HSG', 'Tập đoàn Hoa Sen', 'Steel'),
('VIC', 'Tập đoàn Vingroup', 'Real Estate'),
('VHM', 'Vinhomes', 'Real Estate'),
('MSN', 'Tập đoàn Masan', 'Consumer'),
('SAB', 'Sabeco', 'Consumer');
```

### C. Cấu Trúc Ứng Dụng

```python
# src/main.py - FastAPI Application
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from database import get_db, Database
from models import VPASignal, AlertResponse, PortfolioResponse
from services import VPAAnalyzer, AlertService, PortfolioManager
from auth import verify_token

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/vpa_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="VPA Trading System API",
    description="Professional VPA (Volume Price Analysis) Trading System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting VPA Trading System API...")
    
    # Initialize database
    await Database.initialize()
    
    # Start background tasks
    asyncio.create_task(background_market_scanner())
    asyncio.create_task(background_alert_processor())
    
    logger.info("VPA API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down VPA Trading System API...")
    await Database.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/v1/signals", response_model=List[VPASignal])
async def get_vpa_signals(
    symbol: Optional[str] = None,
    signal_type: Optional[str] = None,
    min_score: Optional[int] = 70,
    limit: int = 50,
    db: Database = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get VPA signals with filters"""
    
    # Verify authentication
    user = await verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        analyzer = VPAAnalyzer(db)
        signals = await analyzer.get_signals(
            symbol=symbol,
            signal_type=signal_type,
            min_score=min_score,
            limit=limit
        )
        
        logger.info(f"Retrieved {len(signals)} VPA signals for user {user['id']}")
        return signals
        
    except Exception as e:
        logger.error(f"Error retrieving VPA signals: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/alerts/subscribe")
async def subscribe_to_alerts(
    alert_config: dict,
    db: Database = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Subscribe to VPA alerts"""
    
    user = await verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        alert_service = AlertService(db)
        subscription = await alert_service.create_subscription(
            user_id=user['id'],
            config=alert_config
        )
        
        return {"message": "Alert subscription created", "subscription_id": subscription.id}
        
    except Exception as e:
        logger.error(f"Error creating alert subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    db: Database = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current portfolio status"""
    
    user = await verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        portfolio_manager = PortfolioManager(db)
        portfolio = await portfolio_manager.get_user_portfolio(user['id'])
        
        return portfolio
        
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/backtest")
async def run_backtest(
    backtest_config: dict,
    background_tasks: BackgroundTasks,
    db: Database = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Run VPA strategy backtest"""
    
    user = await verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Start backtest as background task
    background_tasks.add_task(
        run_backtest_task,
        user_id=user['id'],
        config=backtest_config,
        db=db
    )
    
    return {"message": "Backtest started", "status": "processing"}

async def background_market_scanner():
    """Background task for market scanning"""
    from market_scanner import MarketScanner
    
    scanner = MarketScanner()
    
    while True:
        try:
            await scanner.scan_market()
            await asyncio.sleep(300)  # 5 minutes
        except Exception as e:
            logger.error(f"Market scanner error: {str(e)}")
            await asyncio.sleep(60)  # Wait 1 minute before retry

async def background_alert_processor():
    """Background task for processing alerts"""
    from alert_processor import AlertProcessor
    
    processor = AlertProcessor()
    
    while True:
        try:
            await processor.process_pending_alerts()
            await asyncio.sleep(30)  # 30 seconds
        except Exception as e:
            logger.error(f"Alert processor error: {str(e)}")
            await asyncio.sleep(60)

async def run_backtest_task(user_id: str, config: dict, db: Database):
    """Background backtest execution"""
    from backtester import VPABacktester
    
    try:
        backtester = VPABacktester(db)
        results = await backtester.run_backtest(user_id, config)
        
        # Save results to database
        await backtester.save_backtest_results(user_id, results)
        
        logger.info(f"Backtest completed for user {user_id}")
        
    except Exception as e:
        logger.error(f"Backtest error for user {user_id}: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        access_log=True
    )
```

---

## 📈 Phần 2: Thực Hành - Cloud Deployment

### A. AWS Infrastructure với Terraform

```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
resource "aws_vpc" "vpa_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "vpa-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "vpa_private_subnet" {
  count             = 2
  vpc_id            = aws_vpc.vpa_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "vpa-private-subnet-${count.index + 1}"
    Environment = var.environment
  }
}

resource "aws_subnet" "vpa_public_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.vpa_vpc.id
  cidr_block              = "10.0.${count.index + 10}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "vpa-public-subnet-${count.index + 1}"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "vpa_cluster" {
  name = "vpa-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "vpa-cluster"
    Environment = var.environment
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "vpa_database" {
  identifier = "vpa-database"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = "vpa_db"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.vpa_db_subnet_group.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "vpa-database-final-snapshot"
  
  tags = {
    Name = "vpa-database"
    Environment = var.environment
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "vpa_redis_subnet_group" {
  name       = "vpa-redis-subnet-group"
  subnet_ids = aws_subnet.vpa_private_subnet[*].id
}

resource "aws_elasticache_cluster" "vpa_redis" {
  cluster_id           = "vpa-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.vpa_redis_subnet_group.name
  security_group_ids   = [aws_security_group.redis_sg.id]

  tags = {
    Name = "vpa-redis"
    Environment = var.environment
  }
}

# Application Load Balancer
resource "aws_lb" "vpa_alb" {
  name               = "vpa-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.vpa_public_subnet[*].id

  enable_deletion_protection = false

  tags = {
    Name = "vpa-alb"
    Environment = var.environment
  }
}

# ECS Service
resource "aws_ecs_service" "vpa_api_service" {
  name            = "vpa-api-service"
  cluster         = aws_ecs_cluster.vpa_cluster.id
  task_definition = aws_ecs_task_definition.vpa_api_task.arn
  desired_count   = 2

  launch_type = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.vpa_private_subnet[*].id
    security_groups = [aws_security_group.ecs_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.vpa_api_tg.arn
    container_name   = "vpa-api"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.vpa_api_listener]

  tags = {
    Name = "vpa-api-service"
    Environment = var.environment
  }
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "vpa_logs" {
  name              = "/ecs/vpa-system"
  retention_in_days = 14

  tags = {
    Name = "vpa-logs"
    Environment = var.environment
  }
}
```

### B. CI/CD Pipeline với GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy VPA System

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AWS_REGION: ap-southeast-1
  ECR_REPOSITORY: vpa-system
  ECS_SERVICE: vpa-api-service
  ECS_CLUSTER: vpa-cluster

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
          
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run linting
      run: |
        black --check src/
        flake8 src/
        mypy src/

    - name: Run tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build-and-deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        # Build Docker image
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
        
        # Push to ECR
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
        
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

    - name: Download task definition
      run: |
        aws ecs describe-task-definition \
          --task-definition vpa-api-task \
          --query taskDefinition > task-definition.json

    - name: Update task definition
      id: task-def
      uses: aws-actions/amazon-ecs-render-task-definition@v1
      with:
        task-definition: task-definition.json
        container-name: vpa-api
        image: ${{ steps.build-image.outputs.image }}

    - name: Deploy to Amazon ECS
      uses: aws-actions/amazon-ecs-deploy-task-definition@v1
      with:
        task-definition: ${{ steps.task-def.outputs.task-definition }}
        service: ${{ env.ECS_SERVICE }}
        cluster: ${{ env.ECS_CLUSTER }}
        wait-for-service-stability: true

    - name: Run database migrations
      run: |
        aws ecs run-task \
          --cluster ${{ env.ECS_CLUSTER }} \
          --task-definition vpa-migration-task \
          --launch-type FARGATE \
          --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"

    - name: Notify deployment success
      if: success()
      run: |
        curl -X POST -H 'Content-type: application/json' \
          --data '{"text":"✅ VPA System deployed successfully to production!"}' \
          ${{ secrets.SLACK_WEBHOOK_URL }}

    - name: Notify deployment failure
      if: failure()
      run: |
        curl -X POST -H 'Content-type: application/json' \
          --data '{"text":"❌ VPA System deployment failed! Check GitHub Actions for details."}' \
          ${{ secrets.SLACK_WEBHOOK_URL }}
```

### C. Monitoring & Observability

```python
# src/monitoring.py
import time
import psutil
import asyncio
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from functools import wraps
import logging
from datetime import datetime

# Prometheus metrics
vpa_signals_generated = Counter('vpa_signals_generated_total', 'Total VPA signals generated', ['signal_type', 'symbol'])
vpa_alerts_sent = Counter('vpa_alerts_sent_total', 'Total VPA alerts sent', ['channel', 'priority'])
api_requests = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration', ['method', 'endpoint'])

portfolio_value = Gauge('portfolio_value_total', 'Current portfolio value')
active_positions = Gauge('active_positions_count', 'Number of active positions')
system_cpu_usage = Gauge('system_cpu_usage_percent', 'System CPU usage')
system_memory_usage = Gauge('system_memory_usage_percent', 'System memory usage')

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        
    async def start_metrics_server(self, port=8001):
        """Start Prometheus metrics server"""
        start_http_server(port)
        logger.info(f"Metrics server started on port {port}")
        
        # Start background metrics collection
        asyncio.create_task(self.collect_system_metrics())
    
    async def collect_system_metrics(self):
        """Collect system metrics periodically"""
        while True:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                system_cpu_usage.set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                system_memory_usage.set(memory.percent)
                
                logger.debug(f"System metrics - CPU: {cpu_percent}%, Memory: {memory.percent}%")
                
            except Exception as e:
                logger.error(f"Error collecting system metrics: {e}")
            
            await asyncio.sleep(30)  # Collect every 30 seconds

def monitor_api_request(endpoint: str):
    """Decorator to monitor API requests"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            method = "GET"  # Would extract from request in real implementation
            status = "200"
            
            try:
                result = await func(*args, **kwargs)
                return result
                
            except Exception as e:
                status = "500"
                raise
                
            finally:
                duration = time.time() - start_time
                
                # Record metrics
                api_requests.labels(method=method, endpoint=endpoint, status=status).inc()
                api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
                
        return wrapper
    return decorator

def record_vpa_signal(signal_type: str, symbol: str):
    """Record VPA signal generation"""
    vpa_signals_generated.labels(signal_type=signal_type, symbol=symbol).inc()
    logger.info(f"VPA signal recorded: {signal_type} for {symbol}")

def record_alert_sent(channel: str, priority: str):
    """Record alert sent"""
    vpa_alerts_sent.labels(channel=channel, priority=priority).inc()
    logger.info(f"Alert sent recorded: {channel} - {priority}")

def update_portfolio_metrics(total_value: float, positions_count: int):
    """Update portfolio metrics"""
    portfolio_value.set(total_value)
    active_positions.set(positions_count)

# Health check implementation
class HealthChecker:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
        self.startup_time = datetime.now()
        
    async def health_check(self):
        """Comprehensive health check"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.startup_time).total_seconds(),
            "checks": {}
        }
        
        # Database check
        try:
            await self.db.execute("SELECT 1")
            health_status["checks"]["database"] = "healthy"
        except Exception as e:
            health_status["checks"]["database"] = f"unhealthy: {str(e)}"
            health_status["status"] = "unhealthy"
        
        # Redis check
        try:
            await self.redis.ping()
            health_status["checks"]["redis"] = "healthy"
        except Exception as e:
            health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
            health_status["status"] = "unhealthy"
        
        # System resources check
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > 90:
            health_status["checks"]["cpu"] = f"warning: {cpu_percent}%"
        else:
            health_status["checks"]["cpu"] = f"healthy: {cpu_percent}%"
            
        if memory_percent > 90:
            health_status["checks"]["memory"] = f"warning: {memory_percent}%"
            health_status["status"] = "degraded"
        else:
            health_status["checks"]["memory"] = f"healthy: {memory_percent}%"
        
        return health_status
```

---

## 🔍 Phần 3: Nâng Cao - Production Optimization

> 💡 **Lưu ý**: Phần này dành cho production optimization và scalability. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### A. Auto-Scaling & Performance Optimization

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vpa-api
  labels:
    app: vpa-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vpa-api
  template:
    metadata:
      labels:
        app: vpa-api
    spec:
      containers:
      - name: vpa-api
        image: your-registry/vpa-system:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: vpa-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: vpa-secrets
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: vpa-api-service
spec:
  selector:
    app: vpa-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vpa-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vpa-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### B. Tối Ưuu Hóa Data Pipeline

```python
# src/optimized_data_pipeline.py
import asyncio
import aiohttp
import pandas as pd
from asyncio import Semaphore
from typing import List, Dict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class OptimizedDataPipeline:
    def __init__(self, max_concurrent_requests=10):
        self.session = None
        self.semaphore = Semaphore(max_concurrent_requests)
        self.cache = {}  # Simple in-memory cache
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=20,  # Connections per host
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(
            total=30,  # Total timeout
            connect=10,  # Connection timeout
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_stock_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Fetch stock data with caching and rate limiting"""
        
        cache_key = f"{symbol}_{days}_{datetime.now().date()}"
        
        # Check cache first
        if cache_key in self.cache:
            logger.debug(f"Cache hit for {symbol}")
            return self.cache[cache_key]
        
        async with self.semaphore:  # Rate limiting
            try:
                # Mock API call - replace with actual data source
                url = f"https://api.example.com/stocks/{symbol}"
                params = {"days": days}
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        df = pd.DataFrame(data)
                        
                        # Cache the result
                        self.cache[cache_key] = df
                        
                        logger.info(f"Fetched data for {symbol}: {len(df)} rows")
                        return df
                    else:
                        logger.error(f"Failed to fetch {symbol}: HTTP {response.status}")
                        return pd.DataFrame()
                        
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                return pd.DataFrame()
    
    async def batch_process_vpa_analysis(self, symbols: List[str]) -> Dict[str, dict]:
        """Process VPA analysis for multiple symbols concurrently"""
        
        # Create tasks for concurrent execution
        tasks = []
        for symbol in symbols:
            task = asyncio.create_task(self.process_single_symbol(symbol))
            tasks.append((symbol, task))
        
        results = {}
        
        # Process results as they complete
        for symbol, task in tasks:
            try:
                result = await task
                results[symbol] = result
                logger.info(f"Completed VPA analysis for {symbol}")
                
            except Exception as e:
                logger.error(f"Failed VPA analysis for {symbol}: {e}")
                results[symbol] = {"error": str(e)}
        
        return results
    
    async def process_single_symbol(self, symbol: str) -> dict:
        """Process VPA analysis for a single symbol"""
        
        # Fetch data
        df = await self.fetch_stock_data(symbol)
        
        if df.empty:
            return {"error": "No data available"}
        
        # Run VPA analysis
        vpa_analyzer = VPAAnalyzer()
        analysis_result = await vpa_analyzer.analyze_symbol(symbol, df)
        
        return analysis_result
    
    async def real_time_data_stream(self, symbols: List[str]):
        """Real-time data streaming with WebSocket"""
        
        import websockets
        
        async def handle_websocket_data():
            uri = "wss://api.example.com/realtime"
            
            try:
                async with websockets.connect(uri) as websocket:
                    # Subscribe to symbols
                    subscribe_message = {
                        "action": "subscribe",
                        "symbols": symbols
                    }
                    await websocket.send(json.dumps(subscribe_message))
                    
                    # Process incoming data
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            await self.process_realtime_data(data)
                            
                        except Exception as e:
                            logger.error(f"Error processing real-time data: {e}")
                            
            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
                # Implement reconnection logic
                await asyncio.sleep(5)
                await handle_websocket_data()  # Reconnect
        
        # Start WebSocket handler
        await handle_websocket_data()
    
    async def process_realtime_data(self, data: dict):
        """Process real-time market data"""
        
        symbol = data.get("symbol")
        price = data.get("price")
        volume = data.get("volume")
        timestamp = data.get("timestamp")
        
        # Update real-time cache
        if symbol:
            # Trigger real-time VPA analysis if significant change
            price_change = self.calculate_price_change(symbol, price)
            volume_ratio = self.calculate_volume_ratio(symbol, volume)
            
            if abs(price_change) > 0.02 or volume_ratio > 2.0:  # 2% price or 2x volume
                logger.info(f"Significant change detected for {symbol}: price {price_change:.2%}, volume {volume_ratio:.1f}x")
                
                # Trigger real-time VPA analysis
                await self.trigger_realtime_vpa_analysis(symbol, data)
    
    def calculate_price_change(self, symbol: str, current_price: float) -> float:
        """Calculate price change from previous close"""
        # Implementation would access cached previous price
        # Return mock value for now
        return 0.01  # 1% change
    
    def calculate_volume_ratio(self, symbol: str, current_volume: int) -> float:
        """Calculate volume ratio vs average"""
        # Implementation would access historical volume data
        # Return mock value for now
        return 1.5  # 1.5x average volume
    
    async def trigger_realtime_vpa_analysis(self, symbol: str, market_data: dict):
        """Trigger real-time VPA analysis"""
        
        # Quick VPA analysis for real-time data
        quick_vpa_result = await self.quick_vpa_analysis(symbol, market_data)
        
        if quick_vpa_result.get("signal_detected"):
            # Send real-time alert
            await self.send_realtime_alert(symbol, quick_vpa_result)
    
    async def quick_vpa_analysis(self, symbol: str, market_data: dict) -> dict:
        """Quick VPA analysis for real-time processing"""
        
        # Simplified VPA logic for speed
        volume_ratio = market_data.get("volume_ratio", 1.0)
        price_change = market_data.get("price_change", 0.0)
        
        signal_detected = False
        signal_type = None
        confidence = 0.0
        
        # Simple signal detection
        if volume_ratio > 2.5 and price_change > 0.015:  # Volume spike + price up
            signal_detected = True
            signal_type = "No Supply"
            confidence = min(0.8, volume_ratio / 5.0)
            
        elif volume_ratio > 3.0 and abs(price_change) < 0.005:  # High volume, stable price
            signal_detected = True
            signal_type = "Stopping Volume"
            confidence = min(0.9, volume_ratio / 4.0)
        
        return {
            "signal_detected": signal_detected,
            "signal_type": signal_type,
            "confidence": confidence,
            "volume_ratio": volume_ratio,
            "price_change": price_change,
            "timestamp": datetime.now().isoformat()
        }
    
    async def send_realtime_alert(self, symbol: str, vpa_result: dict):
        """Send real-time VPA alert"""
        
        alert_message = {
            "type": "REALTIME_VPA_SIGNAL",
            "symbol": symbol,
            "signal_type": vpa_result["signal_type"],
            "confidence": vpa_result["confidence"],
            "timestamp": vpa_result["timestamp"],
            "priority": "HIGH" if vpa_result["confidence"] > 0.7 else "MEDIUM"
        }
        
        # Send to alert system
        from alert_system import AlertSystem
        alert_system = AlertSystem()
        await alert_system.send_alert(alert_message)
        
        logger.info(f"Real-time alert sent for {symbol}: {vpa_result['signal_type']}")

# Usage example
async def main():
    """Main data pipeline execution"""
    
    symbols = ["VCB", "TCB", "HPG", "VIC", "SAB"]
    
    async with OptimizedDataPipeline(max_concurrent_requests=20) as pipeline:
        
        # Batch process VPA analysis
        logger.info("Starting batch VPA analysis...")
        batch_results = await pipeline.batch_process_vpa_analysis(symbols)
        
        for symbol, result in batch_results.items():
            if "error" not in result:
                logger.info(f"{symbol}: {result.get('signal_count', 0)} signals detected")
        
        # Start real-time processing
        logger.info("Starting real-time data stream...")
        await pipeline.real_time_data_stream(symbols)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📋 Tóm Tắt Chương

### Production Architecture Hoàn Chỉnh:

#### 🏗️ **Infrastructure Stack:**
- **Container Orchestration:** Docker + Kubernetes/ECS
- **Database:** PostgreSQL (RDS) với read replicas
- **Cache:** Redis (ElastiCache) cho real-time data
- **Load Balancer:** Application Load Balancer với SSL
- **CDN:** CloudFront cho static assets
- **Storage:** S3 cho backups và logs

#### 🔄 **CI/CD Pipeline:**
- **Version Control:** GitHub với branch protection
- **Testing:** Automated unit + integration tests
- **Security:** Trivy scanning + SAST/DAST
- **Deployment:** Zero-downtime rolling updates
- **Rollback:** Automatic rollback trên failure

#### 📊 **Monitoring & Observability:**
- **Metrics:** Prometheus + Grafana dashboards
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing:** Distributed tracing với Jaeger
- **Alerts:** PagerDuty integration cho critical issues
- **Health Checks:** Multi-layer health monitoring

#### 🚀 **Performance Optimizations:**
- **Auto-scaling:** HPA dựa trên CPU/Memory/Custom metrics
- **Caching Strategy:** Multi-level caching (Redis, CDN, Application)
- **Database Optimization:** Connection pooling, query optimization
- **Async Processing:** Event-driven architecture với message queues
- **Rate Limiting:** API rate limiting để bảo vệ resources

#### 🔒 **Security & Compliance:**
- **Authentication:** JWT tokens với refresh mechanism
- **Authorization:** Role-based access control (RBAC)
- **Encryption:** TLS 1.3, encrypted storage
- **Secrets Management:** AWS Secrets Manager/HashiCorp Vault
- **Compliance:** SOC 2, GDPR compliance measures

#### 💾 **Data Management:**
- **Backup Strategy:** Automated daily backups với 30-day retention
- **Disaster Recovery:** Cross-region replication
- **Data Pipeline:** Real-time và batch processing
- **Data Quality:** Validation và monitoring
- **Archival:** Automated archival của old data

### Production Checklist:

#### Pre-Launch:
- [ ] Load testing với realistic traffic
- [ ] Security penetration testing
- [ ] Disaster recovery testing
- [ ] Documentation completion
- [ ] Team training on monitoring/alerts

#### Launch Day:
- [ ] Blue-green deployment setup
- [ ] Monitoring dashboards active
- [ ] Alert systems configured
- [ ] Support team on standby
- [ ] Rollback plan ready

#### Post-Launch:
- [ ] Performance monitoring
- [ ] Cost optimization review
- [ ] User feedback collection
- [ ] Iterative improvements
- [ ] Capacity planning

### Cost Optimization Strategies:
- **Right-sizing:** Regular review của instance sizes
- **Reserved Instances:** Long-term commitments cho cost savings
- **Spot Instances:** Non-critical workloads
- **Storage Optimization:** Lifecycle policies cho S3
- **Monitoring:** Cost alerts và budget controls

### Scaling Strategy:
- **Horizontal Scaling:** Auto-scaling groups
- **Vertical Scaling:** Instance upgrades when needed
- **Database Scaling:** Read replicas, sharding
- **Geographic Scaling:** Multi-region deployment
- **Performance Scaling:** CDN, caching optimizations

### 🎊 Kết Luận Series:

Chúc mừng! Bạn đã hoàn thành toàn bộ series **"VPA & Wyckoff Method cho Thị Trường Việt Nam"** từ beginner đến expert level:

1. **Chương 1-4:** Nền tảng VPA/Wyckoff cơ bản
2. **Chương 5.1-5.9:** Advanced techniques và production system

Bạn hiện có đầy đủ kiến thức và tools để:
- ✅ Phân tích VPA chuyên nghiệp
- ✅ Xây dựng trading systems tự động
- ✅ Deploy production-ready applications
- ✅ Quản lý portfolio hiệu quả
- ✅ Monitor và optimize performance

**Next Steps:**
- Implement system theo từng phase
- Start với paper trading
- Gradually scale to real money
- Continuous learning và improvement

**Remember:** VPA là skill cần practice lâu dài. Hệ thống chỉ là tool hỗ trợ, kiến thức và experience của bạn mới là yếu tố quyết định thành công! 🚀