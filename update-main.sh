#!/bin/bash
git checkout main
git pull origin main
git merge tests
git push origin main --force
git checkout tests
