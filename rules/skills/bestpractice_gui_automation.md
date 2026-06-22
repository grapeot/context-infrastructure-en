# GUI Automation Methodology

Make an API Out of Things That Don't Provide an API.

## Core Idea

Many systems don't provide APIs, but through developer tools, Bookmarklets, Playwright, and other tools, you can turn interfaces without APIs into programmable interfaces.

## Technical Paths

### 1. Dev Tools + HAR Export

Dynamic pages (e.g., infinite scroll) have HTML elements that are dynamically removed. Solution:

1. Open Dev Tools → Network Tab
2. Perform the operation
3. Export HAR
4. Programmatically parse the HAR file

### 2. Bookmarklet + Vision API

Click a bookmarklet on any web image to invoke AI image description — GUI injection that "hijacks the interface."

### 3. Playwright / Claude Computer Use

Achieve GUI automation through VM screenshots + pixel operations. Suitable for scenarios with no API at all.

### Human-AI Loop Breakpoint

When manual screenshot pasting is required, the automation chain breaks. Solution:

- Let AI take screenshots itself (Playwright)
- Use screenshot utilities for automatic capture
