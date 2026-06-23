---
version: alpha
name: "{{PROJECT_NAME}}"
description: >-
  {{PROJECT_DESCRIPTION}} 的基础视觉系统。
colors:
  primary: "#2563EB"
  primary-soft: "#DBEAFE"
  primary-deep: "#1D4ED8"
  surface: "#FFFFFF"
  surface-muted: "#F8FAFC"
  surface-subtle: "#F1F5F9"
  text: "#0F172A"
  text-muted: "#475569"
  border: "#CBD5E1"
  focus: "#7C3AED"
  success: "#16A34A"
  warning: "#D97706"
  danger: "#DC2626"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 40px
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: 0px
  heading:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 28px
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: 0px
  body:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0px
  label:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  caption:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  button-primary-hover:
    backgroundColor: "{colors.primary-deep}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  button-soft:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary-deep}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  page:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  card-subtle:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.text-muted}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  focus-indicator:
    backgroundColor: "{colors.focus}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs}"
  status-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.text}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.sm}"
  status-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.text}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.sm}"
  status-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.surface}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "{spacing.xs} {spacing.sm}"
---

# {{PROJECT_NAME}} Design System

## Overview

本文件是 `{{PROJECT_NAME}}` 的视觉系统入口。Agent 在处理 UI、前端页面、组件样式、响应式布局或设计还原任务时，应先读取本文件，再结合项目已有组件和技术栈实现。

这是一套中性的产品型基础风格：界面应清晰、克制、可扫描，优先服务真实工作流和信息层级，不为了装饰牺牲可读性。

## Colors

- **Primary** (`{colors.primary}`)：主要操作、关键链接和当前状态。
- **Surface** (`{colors.surface}` / `{colors.surface-muted}`)：页面和容器背景。
- **Text** (`{colors.text}` / `{colors.text-muted}`)：正文、辅助说明和元信息。
- **Border** (`{colors.border}`)：分隔线、输入框和低强度容器边界。
- **Focus** (`{colors.focus}`)：键盘焦点、可访问性高亮和临时强调。

## Typography

所有界面文字默认使用系统 sans-serif 栈。标题应表达清晰层级，正文优先保证阅读舒适度。不要用过度夸张的字号填充普通工具界面。

## Layout

使用 4px 基础步进的间距系统。重复元素之间保持稳定节奏；复杂页面优先使用明确的网格、列表和分组，而不是堆叠装饰性卡片。

## Elevation & Depth

默认用边框、背景层级和留白表达结构。阴影只用于弹窗、浮层和需要脱离页面层级的临时界面。

## Shapes

按钮、输入框和卡片默认使用 8px 圆角。图标按钮、头像或状态点可以使用 full radius。不要在同一界面混用过多不同圆角。

## Components

- **Primary button**：每个视图只保留少量最高优先级主按钮。
- **Secondary button**：用于取消、返回、筛选、导出等次级操作。
- **Card**：只用于独立对象、重复列表项、工具面板或弹窗内容，不要把整页 section 都做成浮动卡片。
- **Input**：必须有清晰 label、错误状态和可访问的 focus 状态。

## Do's and Don'ts

- Do 保持文字可读、对比充足、状态明确。
- Do 复用项目已有组件、token 和 CSS 变量。
- Do 在移动端优先保证内容不重叠、按钮可点击、表单可完成。
- Don't 使用真实品牌、账号、密钥、客户信息或私有设计资产作为默认样式。
- Don't 用大面积单一色相、装饰性渐变或无意义背景图掩盖信息结构。
- Don't 为了套用本文件而推翻项目已有成熟设计系统；已有系统优先，本文件用于补足缺口。
