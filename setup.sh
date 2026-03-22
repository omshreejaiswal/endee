#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AI Travel Planner - Endee Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker is not installed${NC}"
        echo "Install Docker from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker is installed${NC}"
}

# Check if Docker daemon is running
check_docker_daemon() {
    if ! docker info &> /dev/null; then
        echo -e "${RED}✗ Docker daemon is not running${NC}"
        echo "Start Docker Desktop or run: docker daemon"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker daemon is running${NC}"
}

# Option 1: Docker Compose (Recommended)
setup_docker() {
    echo -e "\n${YELLOW}Setting up with Docker Compose...${NC}"
    
    cd "$(dirname "$0")"
    
    # Check environment
    if [ ! -f .env ]; then
        echo -e "${YELLOW}Creating .env file...${NC}"
        cp .env.example .env || echo "GROQ_API_KEY=your_key_here" > .env
    fi
    
    # Build backend
    echo -e "${YELLOW}Building backend...${NC}"
    docker-compose build backend
    
    # Start services
    echo -e "${YELLOW}Starting services...${NC}"
    docker-compose up -d
    
    # Wait for services
    echo -e "${YELLOW}Waiting for services to start...${NC}"
    sleep 5
    
    # Check backend health
    if curl -s http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}✓ Backend is running on http://localhost:8000${NC}"
    else
        echo -e "${RED}✗ Backend failed to start${NC}"
        docker-compose logs backend
        exit 1
    fi
    
    # Check frontend
    if curl -s http://localhost:3000/ > /dev/null; then
        echo -e "${GREEN}✓ Frontend is running on http://localhost:3000${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend is starting, wait a moment...${NC}"
    fi
    
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Services started successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "Frontend: ${BLUE}http://localhost:3000${NC}"
    echo -e "Backend API: ${BLUE}http://localhost:8000${NC}"
    echo -e "API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo "View logs:"
    echo "  docker-compose logs -f backend"
    echo ""
    echo "Stop services:"
    echo "  docker-compose down"
    echo ""
}

# Option 2: Local Python
setup_local() {
    echo -e "\n${YELLOW}Setting up with Local Python...${NC}"
    
    cd "$(dirname "$0")"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python 3 is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python 3 is available${NC}"
    
    # Create/activate venv
    if [ ! -d venv ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
    
    # Install dependencies
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r Backend/requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    
    # Start backend
    echo -e "${YELLOW}Starting backend...${NC}"
    cd Backend
    python3 main.py &
    BACKEND_PID=$!
    cd ..
    
    sleep 3
    
    if curl -s http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}✓ Backend is running (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${RED}✗ Backend failed to start${NC}"
        exit 1
    fi
    
    # Start frontend
    echo -e "${YELLOW}Starting frontend...${NC}"
    cd frontend
    python3 -m http.server 3000 > /dev/null 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    sleep 2
    echo -e "${GREEN}✓ Frontend is running (PID: $FRONTEND_PID)${NC}"
    
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Services started locally!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "Frontend: ${BLUE}http://localhost:3000${NC}"
    echo -e "Backend API: ${BLUE}http://localhost:8000${NC}"
    echo ""
    echo "Stop services:"
    echo "  kill $BACKEND_PID $FRONTEND_PID"
    echo ""
}

# Main
echo ""
echo "Select setup option:"
echo "1. Docker Compose (Recommended - easy, isolated)"
echo "2. Local Python (Direct - fast, no Docker needed)"
echo ""
read -p "Enter option (1 or 2): " option

case $option in
    1)
        check_docker
        check_docker_daemon
        setup_docker
        ;;
    2)
        setup_local
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo -e "${BLUE}For more information, see:${NC}"
echo "  - RUN_PROJECT.md"
echo "  - ENDEE_VERIFICATION.md"
echo "  - HOW_TO_RUN.md"
echo ""
