---
layout: default
title: "Developer Guides"
description: "Comprehensive guides for development tools and best practices"
---

# 📚 Developer Guides

Essential guides and tutorials to help you set up and optimize your development environment.

<div class="features">
{% for guide in site.guides %}
    <div class="feature">
        <h3><a href="{{ guide.url | relative_url }}">{{ guide.title }}</a></h3>
        <p>{{ guide.description }}</p>
        <p><strong>Category:</strong> {{ guide.category }}</p>
        <a href="{{ guide.url | relative_url }}" class="btn">Read Guide</a>
    </div>
{% endfor %}
</div>

## 🎯 Guide Categories

Our guides cover essential development tools and practices:

- **Development Tools**: VS Code, IDE configuration, and editor setup
- **Best Practices**: Code quality, documentation, and workflow optimization
- **Environment Setup**: Development environment configuration
- **Troubleshooting**: Common issues and solutions

<div style="text-align: center; margin: 3rem 0;">
    <a href="{{ '/' | relative_url }}" class="btn">← Back to Home</a>
</div>