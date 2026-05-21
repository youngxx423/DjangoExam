# eBay官网复现

## 📁 目录结构树

```text
Ebay_Project
│
├── 📄 index.html          # [首页] 包含轮播图、搜索栏、商品分类展示
├── 📄 login.html          # [登录页] 包含表单验证 (正则校验邮箱/密码)
├── 📄 register.html       # [注册页] (可选，也可合并在login中) 用户注册逻辑
├── 📄 detail.html         # [商品详情页] 展示商品大图、规格、加入购物车按钮
├── 📄 cart.html           # [购物车页] 展示已选商品、修改数量、删除商品
├── 📄 checkout.html       # [结算/订单页] 模拟提交订单、支付界面
├── 📄 profile.html        # [个人中心页] 显示用户信息、模拟的订单记录
│
├── 📂 css/                # [样式文件夹]
│   ├── 📄 style.css       # 全局通用样式 (头部、底部、字体)
│   ├── 📄 index.css       # 首页特定样式 (轮播图样式)
│   ├── 📄 detail.css      # 详情页特定样式
│   └── 📄 reset.css       # 浏览器样式重置 (Normalize)
│
├── 📂 js/                 # [脚本文件夹]
│   ├── 📄 main.js         # 公共逻辑 (头部导航交互、搜索跳转)
│   ├── 📄 data.js         # 模拟后端数据库 (存储商品JSON数据)
│   ├── 📄 cart.js         # 购物车逻辑 (LocalStorage增删改查)
│   ├── 📄 auth.js         # 登录注册验证逻辑 (正则校验)
│   └── 📄 carousel.js     # 首页轮播图逻辑
│
└── 📂 images/             # [图片素材]
    ├── 📄 logo.png        # eBay Logo
    ├── 📂 banner/         # 轮播图素材
    │   ├── banner1.jpg
    │   └── banner2.jpg
    └── 📂 products/       # 商品图片
        ├── prod1.jpg
        └── prod2.jpg
```

## 功能要求

功能至少要包括基础逻辑功能，比如网上商城网页至少要包括以下主要功能：

- 首页（包含轮播图、搜索、分类等功能）
- 登录注册页面（登录注册合法性校验）
- 商品详情页
- 购物车页面
- 提交订单页
- 结算页面
- 个人中心页
