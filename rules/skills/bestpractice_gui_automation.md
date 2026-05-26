# GUI 自动化方法论

Make an API Out of Things That Don't Provide an API.

## 核心思路

很多系统没有提供 API，但可以通过开发者工具、Bookmarklet、Playwright 等工具，将无 API 的界面转化为可编程接口。

## 技术路径

### 1. Dev Tools + HAR Export

动态页面（如无限滚动）的 HTML 元素会被动态移除。解决方案：

1. 打开 Dev Tools → Network Tab
2. 执行操作
3. Export HAR
4. 编程解析 HAR 文件

### 2. Bookmarklet + Vision API

在任意网页图片上点击书签即可调用 AI 描述图片内容——"hijack the interface"的 GUI 注入。

### 3. Playwright / Claude Computer Use

通过虚拟机截图 + 像素操作实现 GUI 自动化。适用于无任何 API 的场景。

### Human-AI 循环断裂点

当需要人工截图粘贴时，自动化链条断裂。解决方案：

- 让 AI 自己截图（Playwright）
- 使用 screenshot utilities 自动捕获
