#!/bin/bash

# Exit on error
set -e

IMAGE_NAME="sift-volatility"
DOCKERFILE="Dockerfile.volatility"

echo "[*] Building $IMAGE_NAME image..."

# Check if we are on Apple Silicon and force linux/amd64 if so
# SIFT is primarily built for amd64
PLATFORM="linux/amd64"

docker build --platform "$PLATFORM" -t "$IMAGE_NAME" -f "$DOCKERFILE" .

echo "[+] Build complete: $IMAGE_NAME"
echo "[*] You can now use this image in SIFTOrchestrator by passing image_name='$IMAGE_NAME'"
