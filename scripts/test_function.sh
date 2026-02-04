#!/bin/bash
# Test script for the deployed Arigold agent

set -e

# Configuration
PROJECT_ID="${ARIGOLD_PROJECT_ID:-your-project-id}"
REGION="${ARIGOLD_REGION:-us-central1}"
FUNCTION_NAME="${ARIGOLD_FUNCTION_NAME:-arigold-agent}"

echo "=========================================="
echo "Testing Arigold Agent"
echo "=========================================="

# Get the function URL
FUNCTION_URL=$(gcloud functions describe "$FUNCTION_NAME" \
    --region="$REGION" \
    --gen2 \
    --format="value(serviceConfig.uri)")

echo "Function URL: $FUNCTION_URL"
echo ""

# Test 1: Health check
echo "Test 1: Health check..."
curl -X GET "$FUNCTION_URL/health" -H "Content-Type: application/json"
echo -e "\n"

# Test 2: Simple query
echo "Test 2: Simple query..."
curl -X POST "$FUNCTION_URL" \
    -H "Content-Type: application/json" \
    -d '{
        "request": "What can you help me with?",
        "context": {"user": "test_user"}
    }' | jq '.'
echo ""

# Test 3: Orchestration query
echo "Test 3: Orchestration query..."
curl -X POST "$FUNCTION_URL" \
    -H "Content-Type: application/json" \
    -d '{
        "request": "I need help coordinating multiple tasks. Can you assist?",
        "context": {"task_type": "orchestration"}
    }' | jq '.'
echo ""

echo "=========================================="
echo "Testing completed!"
echo "=========================================="
