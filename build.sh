#!/bin/bash
#
#  build.sh
#  sakotenz.github.io
#
#  Created by Vitor Venturin on 07/11/2026.
#

echo "Building Jekyll site..."

if ! command -v bundle &> /dev/null; then
    echo "Bundle not found. Installing..."
    gem install bundler
fi

echo "Installing dependencies..."
bundle install

echo "Building site..."
bundle exec jekyll build

echo "Build complete! Site generated in _site directory."
echo "To serve locally, run: bundle exec jekyll serve"
