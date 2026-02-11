# 🚀 Production-Grade E-Commerce Application with Full CI/CD Pipeline

![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-blue?logo=jenkins)
![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-AWS%20EKS-blue?logo=kubernetes)
![GitOps](https://img.shields.io/badge/GitOps-ArgoCD-orange?logo=argo)
![Flask](https://img.shields.io/badge/Flask-Python-green?logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![Helm](https://img.shields.io/badge/Helm-Charts-0F1689?logo=helm)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-E6522C?logo=prometheus)
![Grafana](https://img.shields.io/badge/Dashboards-Grafana-F46800?logo=grafana)

---

## 📌 Project Overview

A **full-featured e-commerce web application** built with Flask and deployed using a **production-grade CI/CD pipeline**:

* **Complete E-Commerce Features**: Product catalog, shopping cart, user authentication, payment processing, order tracking
* **Database Integration**: SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL)
* **Payment Gateway**: Stripe integration for secure payments
* **Email Notifications**: Order confirmations and user notifications
* **Admin Dashboard**: Complete product, order, and user management
* **Jenkins Multibranch Pipeline**: Automated CI/CD
* **Docker & DockerHub**: Containerized deployment
* **Helm Package Manager**: Kubernetes application deployment and management
* **Argo CD (GitOps)**: Automated Kubernetes deployments
* **AWS EKS**: Production Kubernetes cluster
* **Prometheus & Grafana**: Complete monitoring and observability stack

This repository demonstrates how **real-world DevOps teams** build, automate, and deploy full-stack applications from **code commit to live production**.

---

## 🎯 Application Features

### 🛒 E-Commerce Functionality
✔ **Product Catalog**: 21 products across 7 categories (Electronics, Fashion, Home, Sports, Books, Toys)
✔ **Smart Search**: Search by name, description, category, and features
✔ **Category Filters**: Quick filtering with icon-based buttons
✔ **Shopping Cart**: Add/remove items, quantity management
✔ **Product Reviews**: Star ratings and customer reviews
✔ **Wishlist**: Save favorite products

### 👤 User Management
✔ **User Registration & Login**: Secure authentication with bcrypt password hashing
✔ **Session Management**: Flask-Login integration
✔ **User Profiles**: Personal information and order history
✔ **My Orders Page**: Track order status with visual timeline

### 💳 Payment & Orders
✔ **Stripe Payment Integration**: Secure payment processing
✔ **Order Tracking**: Real-time status updates (Confirmed → Shipped → Delivered)
✔ **Email Notifications**: Order confirmations sent to customer email
✔ **Payment History**: View all transactions

### 🔧 Admin Dashboard
✔ **Product Management**: Add, edit, delete products with image URLs
✔ **Order Management**: View all orders, update status
✔ **User Management**: View registered users
✔ **Statistics Dashboard**: Total products, orders, users, revenue

### 🎨 Technical Features
✔ **Responsive Design**: Mobile-friendly UI
✔ **Category-Specific Images**: Real product images from Unsplash
✔ **SQLite Database**: Easy setup, no external database required
✔ **Optional Services**: Works without Stripe API keys or email configuration
✔ **Production Ready**: Environment variables, security best practices

---

## 🎯 DevOps & CI/CD Features

✔ Jenkins Multibranch Pipeline with feature branch support
✔ Automated Docker image builds and DockerHub push
✔ Kubernetes deployment with resource limits and health checks
✔ Helm-based package management for Argo CD and monitoring stack
✔ GitOps workflow with Argo CD automated sync
✔ Prometheus & Grafana monitoring with pre-configured dashboards
✔ AWS EKS production cluster deployment
✔ LoadBalancer service for external access
✔ Alertmanager for proactive incident management

---

## 🔁 End-to-End Deployment Flow

```text
Developer
   ↓
Feature Branch (featureA / featureB)
   ↓
Pull Request → Merge to main (GitHub UI)
   ↓
Jenkins Multibranch Pipeline (CI)
   ↓
Build Docker Image + Push to DockerHub
   ↓
Update Image Tag in Git (K8s Manifest Repo)
   ↓
Argo CD Sync (GitOps)
   ↓
AWS EKS Deployment (with Resource Limits & Health Checks)
   ↓
LoadBalancer URL → Live E-Commerce Application
```

---

## 🛠️ Technology Stack

### Backend & Database
| Technology | Purpose |
|------------|---------|
| 🐍 **Flask** | Python web framework |
| �️ *D*SQLAlchemy** | ORM for database operations |
| � ***Flask-Login** | User session management |
| 🔒 **Bcrypt** | Password hashing |
| � **ASQLite** | Database (production-ready, or use PostgreSQL) |

### Frontend
| Technology | Purpose |
|------------|---------|
| 🎨 **HTML/CSS/JS** | Responsive UI |
| 🖼️ **Unsplash API** | Category-specific product images |
| ⚡ **Vanilla JavaScript** | Dynamic cart and filters |

### Payment & Communication
| Technology | Purpose |
|------------|---------|
| 💳 **Stripe** | Payment processing |
| 📧 **Flask-Mail** | Email notifications |

### DevOps & Deployment
| Tool | Purpose |
|------|---------|
| 🐙 **GitHub** | Feature branches, Pull Requests, Source Control |
| 🧩 **Jenkins Multibranch Pipeline** | Continuous Integration (CI) |
| 🐳 **Docker** | Containerization |
| 📦 **DockerHub** | Image Registry |
| ☸️ **Kubernetes (AWS EKS)** | Container Orchestration with Resource Management |
| � **Helm** |* Kubernetes package manager for Argo CD and monitoring |
| 🔄 **Argo CD** | GitOps-based Continuous Deployment |
| 🌐 **LoadBalancer Service** | External Application Access |

### Monitoring & Observability
| Tool | Purpose |
|------|---------|
| 📈 **Prometheus** | Metrics collection and time-series database |
| 📊 **Grafana** | Visualization dashboards and analytics |
| 🔔 **Alertmanager** | Alert routing and management |
| 📡 **Node Exporter** | Hardware and OS metrics collection |
| 🎯 **Kube State Metrics** | Kubernetes cluster state metrics |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Docker (for containerization)
- Kubernetes cluster (for deployment)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Production-Grade-Deployment/Main\ Branch\ Code
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Generate a secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Create .env file (already provided)
# Update SECRET_KEY with generated key
# Optional: Add Stripe keys and email config
```

4. **Run the application**
```bash
python app_enhanced.py
```

5. **Access the application**
- Main site: `http://localhost:5000`
- Admin panel: `http://localhost:5000/admin`
- Default admin: username=`admin`, password=`admin123`

### Environment Variables

```env
# Required
SECRET_KEY=your-generated-secret-key

# Optional - Payment (works without these)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Optional - Email (works without these)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Docker Deployment

```bash
# Build image
docker build -t your-username/ecommerce-app:latest .

# Run container
docker run -p 5000:5000 --env-file .env your-username/ecommerce-app:latest
```

### Kubernetes Deployment

```bash
# Apply deployment (includes resource limits and health checks)
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get svc
```

---

## 👥 Who Is This Project For?

✅ DevOps Engineers learning CI/CD pipelines
✅ Full-Stack Developers building e-commerce applications
✅ Jenkins Multibranch Pipeline learners
✅ Kubernetes & AWS EKS users
✅ GitOps & Argo CD enthusiasts
✅ DevOps interview preparation
✅ Anyone wanting to learn production-grade deployments

---

## 📁 Project Structure

```
Production-Grade-Deployment/
├── Main Branch Code/           # Main application code
│   ├── app_enhanced.py        # Main Flask application
│   ├── models.py              # Database models
│   ├── config.py              # Configuration
│   ├── forms.py               # WTForms
│   ├── templates.py           # HTML templates
│   ├── templates_orders.py    # Orders page template
│   ├── email_utils.py         # Email functions
│   ├── payment_utils.py       # Stripe integration
│   ├── static/
│   │   ├── app.js            # Frontend JavaScript
│   │   └── admin.js          # Admin panel JS
│   ├── k8s/
│   │   ├── deployment.yaml   # K8s deployment with resource limits
│   │   └── service.yaml      # LoadBalancer service
│   ├── argocd/
│   │   └── application.yaml  # Argo CD config
│   ├── Dockerfile            # Container image
│   ├── Jenkinsfile           # CI/CD pipeline
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables
├── FeatureA Branch Code/      # Demo: Wishlist feature
└── FeatureB Branch Code/      # Demo: Order tracking feature
```

---

## 🔐 Security Features

✅ Bcrypt password hashing
✅ CSRF protection with Flask-WTF
✅ SQL injection prevention with SQLAlchemy ORM
✅ Secure session management
✅ Environment variable configuration
✅ Optional Stripe payment security
✅ Kubernetes resource limits to prevent resource exhaustion

---

## 📊 Database Schema

- **Users**: Authentication and profile data
- **Products**: Product catalog with categories and features
- **Orders**: Order information and status tracking
- **OrderItems**: Individual items in each order
- **Reviews**: Product reviews and ratings
- **Wishlist**: User's saved products

---

## 🎨 UI Features

- Responsive design for mobile and desktop
- Category-based product filtering
- Real-time search functionality
- Shopping cart with quantity management
- Visual order status timeline
- Admin dashboard with statistics
- Product image gallery with category-specific images

---

## 🔧 Kubernetes Configuration

The deployment includes production-ready configurations:

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

livenessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 30

readinessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 10
```

---

## 📊 Monitoring & Observability

This project includes production-grade monitoring using **Prometheus** and **Grafana** for complete observability.

### 🔍 Monitoring Stack

| Tool | Purpose |
|------|---------|
| 📈 **Prometheus** | Metrics collection and storage |
| 📊 **Grafana** | Visualization and dashboards |
| 🔔 **Alertmanager** | Alert management and notifications |
| 📡 **Node Exporter** | Hardware and OS metrics |
| 🎯 **Kube State Metrics** | Kubernetes cluster metrics |

---

### 🚀 Setup Monitoring (Prometheus + Grafana)

#### Step 1: Add Helm Repository
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

#### Step 2: Create Monitoring Namespace
```bash
kubectl create namespace monitoring
```

#### Step 3: Install kube-prometheus-stack
```bash
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
```
⏳ Takes 1-2 minutes to deploy all components.

#### Step 4: Verify Installation
```bash
kubectl get pods -n monitoring
```

You should see:
- ✅ Prometheus server
- ✅ Alertmanager
- ✅ Grafana
- ✅ Node exporter
- ✅ Kube-state-metrics

---

### 🌐 Access Grafana Dashboard

#### 1. Expose Grafana via LoadBalancer
```bash
kubectl patch svc monitoring-grafana \
  -n monitoring \
  -p '{"spec":{"type":"LoadBalancer"}}'
```

#### 2. Get Grafana URL
```bash
kubectl get svc monitoring-grafana -n monitoring
```
Open: `http://<EXTERNAL-IP>`

#### 3. Get Grafana Login Credentials
```bash
# Get password
kubectl get secret monitoring-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 -d

# Login credentials
Username: admin
Password: (output from above command)
```

---

### 📈 Pre-configured Dashboards

The kube-prometheus-stack includes **production-ready dashboards** automatically:

| Dashboard | Metrics |
|-----------|---------|
| **Kubernetes / Cluster** | Overall cluster health, resource usage |
| **Kubernetes / Nodes** | Node CPU, memory, disk, network |
| **Kubernetes / Pods** | Pod status, restarts, resource consumption |
| **Kubernetes / Deployments** | Deployment status, replica counts |
| **Node Exporter Full** | Detailed hardware metrics |

👉 **No manual import needed** - All dashboards are auto-configured!

---

### 🎯 Key Metrics to Monitor

#### Application Metrics:
- ✅ Pod CPU and memory usage
- ✅ Request latency and throughput
- ✅ Error rates (4xx, 5xx)
- ✅ Pod restart counts
- ✅ Container health status

#### Infrastructure Metrics:
- ✅ Node resource utilization
- ✅ Disk I/O and network traffic
- ✅ Kubernetes API server health
- ✅ etcd performance
- ✅ Cluster capacity and limits

#### Business Metrics (Custom):
- ✅ Total orders placed
- ✅ Active users
- ✅ Payment success rate
- ✅ Cart abandonment rate

---

### 🔔 Alerting (Optional)

Prometheus Alertmanager is included for notifications:

```bash
# Access Alertmanager
kubectl port-forward svc/monitoring-kube-prometheus-alertmanager \
  -n monitoring 9093:9093
```

Configure alerts for:
- High CPU/memory usage
- Pod crashes or restarts
- Node failures
- Disk space warnings
- Application errors

---

### 📊 Monitoring Architecture

```
Application Pods
      ↓
  Prometheus (scrapes metrics)
      ↓
  Grafana (visualizes)
      ↓
  Alertmanager (sends alerts)
      ↓
  Email/Slack/PagerDuty
```

---

### 🛠️ Useful Monitoring Commands

```bash
# Check Prometheus status
kubectl get pods -n monitoring | grep prometheus

# Check Grafana status
kubectl get svc monitoring-grafana -n monitoring

# View Prometheus targets
kubectl port-forward svc/monitoring-kube-prometheus-prometheus \
  -n monitoring 9090:9090
# Open: http://localhost:9090/targets

# Restart monitoring stack
helm upgrade monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring

# Uninstall monitoring (if needed)
helm uninstall monitoring -n monitoring
kubectl delete namespace monitoring
```

---

### 💡 Monitoring Best Practices

✅ Set up alerts for critical metrics
✅ Monitor resource limits vs actual usage
✅ Track application-specific metrics
✅ Regular dashboard reviews
✅ Set retention policies for metrics
✅ Backup Grafana dashboards
✅ Use labels for better filtering

---

## 📝 Notes

- **Database**: Uses SQLite by default (no setup required). Can easily switch to PostgreSQL for production.
- **Payment**: Stripe integration is optional. App works without API keys for testing.
- **Email**: Email notifications are optional. App works without SMTP configuration.
- **Images**: Product images are fetched from Unsplash API (category-specific).
- **Admin Access**: Default admin credentials are `admin`/`admin123` (change in production).

---

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🎓 Learning Resources

This project demonstrates:
- Full-stack web development with Flask
- Database design and ORM usage
- Payment gateway integration
- Email notification systems
- User authentication and authorization
- Admin panel development
- Docker containerization with multi-stage builds
- Kubernetes deployment with best practices
- Helm package management
- CI/CD pipeline with Jenkins Multibranch
- GitOps with Argo CD
- AWS EKS cluster management
- Prometheus & Grafana monitoring stack
- Production-grade observability and alerting

Perfect for learning modern DevOps practices and full-stack development! 🚀





