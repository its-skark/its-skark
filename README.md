<!--
  ============================================================================
  RACHIT PANDEY — GitHub profile README
  Handle: its-skark   ·   Repo: its-skark/its-skark
  ============================================================================

  WHY TABLE CELLS ARE PURE HTML
  ------------------------------
  Inside a <td>, GFM markdown parsing is inconsistent: a blank line after the
  opening tag starts a markdown block, but an indented closing tag can then be
  swallowed into an indented-code-block and render as literal `</td>`. Verified
  against https://api.github.com/markdown (GitHub's own renderer).

  So: markdown is used freely OUTSIDE tables (headings, lists, paragraphs), and
  every table cell is written in plain HTML (<h3>, <p>, <ul>, <li>, <b>). That
  is deterministic on every renderer and is what the community templates do.

  WHAT GITHUB ALLOWS (verified allowlist)
  --------------------------------------
  Kept:      h1-h6, p, div, span, a, img, picture, source, br, b, strong, em,
             i, small, sub, sup, kbd, abbr, table, thead, tbody, tr, td, th,
             details, summary, blockquote, hr, code, pre, ul, ol, li, dl, dt, dd
  Removed:   iframe, style, script, link, class, style="", object, embed, svg,
             form, and every data: URI. `target` is also stripped.
  Kept attrs: align, width, valign, colspan, open, src, href, alt.

  Consequently there are exactly two visual tools:
    1. layout  -> <table>, <div align="center">, <details>
    2. artwork -> <img src="assets/*.svg">. SVG loaded through <img> keeps its
       CSS @keyframes, SMIL <animate>, gradients and <filter> blurs, which is
       why every decorative element here is a self-hosted SVG.

  NO third-party card services are used for the visuals: github-profile-trophy
  and github-readme-activity-graph both return HTTP 402 (deployments disabled),
  readme-typing-svg's public endpoints now return an HTML demo page instead of
  an SVG, and githack/jsDelivr cannot deliver HTML to a README because iframes
  are stripped. Self-hosted SVG means the design cannot break.

  Regenerate the artwork after editing the generators:
      python3 tools/gen_cards.py assets
      python3 tools/gen_typing_svg.py assets
  Check the README before pushing:
      python3 tools/lint_readme.py
      python3 tools/check_images.py
      python3 tools/preview_readme.py
-->

<p align="center">
  <img src="assets/hero.svg" width="100%" alt="Rachit Pandey — full-stack TypeScript, AI and cloud engineer" />
</p>

<p align="center">
  <img src="assets/typing.svg" width="620" alt="full-stack typescript engineer · angular · react · node · postgres · python · aws" />
</p>

<p align="center">
  <a href="https://github.com/its-skark/SkillFlowApp">
    <img src="assets/status.svg" width="640" alt="currently: POS platforms, SkillFlow AI engine, open to roles" />
  </a>
</p>

<p align="center">
  <a href="https://its-skark.github.io/its-skark/">
    <img alt="Open the full interactive profile site" src="https://img.shields.io/badge/%E2%9C%A8%20full%20interactive%20site-8b5cf6?style=for-the-badge&logo=githubpages&logoColor=white" />
  </a>
  <a href="https://github.com/its-skark">
    <img alt="GitHub followers" src="https://img.shields.io/github/followers/its-skark?style=for-the-badge&label=Followers&color=8b5cf6" />
  </a>
  <img alt="Public repositories" src="https://img.shields.io/badge/repos-20-22d3ee?style=for-the-badge&logo=github&logoColor=white" />
  <img alt="Location: Pantnagar, India" src="https://img.shields.io/badge/pantnagar%2C%20india-8b5cf6?style=for-the-badge&logo=googlemaps&logoColor=white" />
  <img alt="Degree" src="https://img.shields.io/badge/b.tech%20it%20%7C%202026-22d3ee?style=for-the-badge&logo=university&logoColor=white" />
</p>

<img src="assets/divider.svg" width="100%" alt="decorative divider" />

## About me

I build **production web systems** — the kind with tenants, migrations, payment
webhooks, role-based access and a support ticket that says *"it works on my
machine"*. My day job is Angular front-ends and Node/Express services behind
multi-tenant POS products used by real restaurants, hotels and laundries.

On the side I work on **AI-assisted developer tooling**: an engine that parses
repositories with `tree-sitter`, runs `semgrep` rules and scores engineering
practice so recruiters can screen beyond a CV. I've also compiled and maintained
a custom **Linux kernel** for a Poco device — a very different flavour of *"it
won't boot"*.

I like boring, well-named code: explicit schemas over clever inference, boring
infrastructure over heroics, and documentation that survives the next sprint.

<details>
<summary><b>More about my focus</b></summary>

- <b>Production SaaS</b> — multi-tenant POS suites, booking &amp; billing flows, offline-tolerant front-ends, admin consoles
- <b>AI &amp; code intelligence</b> — tree-sitter multi-language AST parsing, semgrep static analysis, MCP tooling, AWS Bedrock prompt/context design
- <b>Cloud &amp; DevOps</b> — EC2 + S3 + DynamoDB, Nginx reverse proxies, Docker builds, Stripe/Razorpay webhooks, Zod validation
- <b>Interface craft</b> — Angular + PrimeNG and React + Tailwind screens that stay fast, accessible and consistent under load

</details>

<details>
<summary><b>What I use daily</b></summary>

<img alt="TypeScript" src="https://img.shields.io/badge/typescript-3178c6?style=flat-square&labelColor=0d1117&logo=typescript&logoColor=white" />
<img alt="Angular" src="https://img.shields.io/badge/angular-20-DD0031?style=flat-square&labelColor=0d1117&logo=angular&logoColor=white" />
<img alt="React" src="https://img.shields.io/badge/react-61DAFB?style=flat-square&labelColor=0d1117&logo=react&logoColor=black" />
<img alt="Node.js" src="https://img.shields.io/badge/node-5FA04E?style=flat-square&labelColor=0d1117&logo=nodedotjs&logoColor=white" />
<img alt="Express" src="https://img.shields.io/badge/express-404040?style=flat-square&labelColor=0d1117&logo=express&logoColor=white" />
<img alt="PostgreSQL" src="https://img.shields.io/badge/postgresql-4169E1?style=flat-square&labelColor=0d1117&logo=postgresql&logoColor=white" />
<img alt="Python" src="https://img.shields.io/badge/python-3776AB?style=flat-square&labelColor=0d1117&logo=python&logoColor=white" />
<img alt="FastAPI" src="https://img.shields.io/badge/fastapi-009688?style=flat-square&labelColor=0d1117&logo=fastapi&logoColor=white" />
<img alt="AWS" src="https://img.shields.io/badge/aws-FF9900?style=flat-square&labelColor=0d1117&logo=amazonaws&logoColor=black" />
<img alt="Docker" src="https://img.shields.io/badge/docker-2496ED?style=flat-square&labelColor=0d1117&logo=docker&logoColor=white" />
<img alt="Tailwind CSS" src="https://img.shields.io/badge/tailwind-38BDF8?style=flat-square&labelColor=0d1117&logo=tailwindcss&logoColor=black" />
<img alt="PrimeNG" src="https://img.shields.io/badge/primeng-A855F7?style=flat-square&labelColor=0d1117" />
<img alt="Git" src="https://img.shields.io/badge/git-F05032?style=flat-square&labelColor=0d1117&logo=git&logoColor=white" />
<img alt="Linux" src="https://img.shields.io/badge/linux-FCC624?style=flat-square&labelColor=0d1117&logo=linux&logoColor=black" />
<img alt="Nginx" src="https://img.shields.io/badge/nginx-009639?style=flat-square&labelColor=0d1117&logo=nginx&logoColor=white" />

</details>

<details>
<summary><b>Currently reading / thinking about</b></summary>

- Multi-tenant Postgres schema design — RLS, tenant isolation, zero-downtime migrations
- Making AI evaluation measurable instead of vibes-based
- Angular signals vs. the rest of the ecosystem
- Why "just add a cache" is never the fix

</details>

<img src="assets/stack.svg" width="100%" alt="Technology stack: TypeScript, Angular, React, Node.js, Express, PostgreSQL, Python, FastAPI, AWS, Docker, tree-sitter, semgrep" />

<img src="assets/divider.svg" width="100%" alt="decorative divider" />

## Featured work

<table>
<tr>
<td width="50%" valign="top">

<h3>SkillFlow — AI-powered technical hiring</h3>

My B.Tech major project. A hiring platform that evaluates candidates on
<b>repository intelligence</b> instead of resume keywords: candidates submit their
strongest repos, and the engine parses them, scores engineering practice and
drives the recruiter's pipeline from there.

<ul>
<li><b>tree-sitter AST parsing</b> for C, Go, Java, JavaScript, Python, Ruby, Rust and TypeScript — real structure, not regex</li>
<li><b>FastAPI service</b> with Pydantic schemas, OpenTelemetry tracing and an MCP server for agent tooling</li>
<li><b>Configurable funnels</b>: stage transitions, automation rules, ATS filtering, assessment scheduling and manual review</li>
<li><b>semgrep static analysis</b> plus weighted scoring across complexity, activity and language mix</li>
</ul>

<p>
<img alt="Python" src="https://img.shields.io/badge/python-3776AB?style=flat-square&labelColor=0d1117&logo=python&logoColor=white" />
<img alt="FastAPI" src="https://img.shields.io/badge/fastapi-009688?style=flat-square&labelColor=0d1117&logo=fastapi&logoColor=white" />
<img alt="tree-sitter" src="https://img.shields.io/badge/tree--sitter-a8d6ba?style=flat-square&labelColor=0d1117" />
<img alt="semgrep" src="https://img.shields.io/badge/semgrep-c4b5fd?style=flat-square&labelColor=0d1117" />
<img alt="MySQL" src="https://img.shields.io/badge/mysql-4479A1?style=flat-square&labelColor=0d1117&logo=mysql&logoColor=white" />
</p>

<p>
<a href="https://github.com/its-skark/SkillFlowApp"><img alt="SkillFlowApp source" src="https://img.shields.io/badge/github-1e1e1e?style=for-the-badge&logo=github&logoColor=white" /></a>
<a href="https://github.com/its-skark/source_analytics_engine"><img alt="source_analytics_engine source" src="https://img.shields.io/badge/analytics%20engine-1e1e1e?style=for-the-badge&logo=githubactions&logoColor=white" /></a>
</p>

</td>
<td width="50%" valign="top">

<h3>Restaurant · Hotel · Laundry POS</h3>

A multi-tenant POS platform family: order and billing flows, kitchen / barcode /
QR printing, subscriptions, org-level settings, and an Express API split into
focused services (users, bookings, organisations, settings, customers) on
PostgreSQL. Built with <b>Angular 20</b> + PrimeNG + Tailwind on the front,
Express + PostgreSQL behind it, in Docker.

<p>
<img alt="Angular" src="https://img.shields.io/badge/angular-DD0031?style=flat-square&labelColor=0d1117&logo=angular&logoColor=white" />
<img alt="PrimeNG" src="https://img.shields.io/badge/primeng-A855F7?style=flat-square&labelColor=0d1117" />
<img alt="Tailwind" src="https://img.shields.io/badge/tailwind-38BDF8?style=flat-square&labelColor=0d1117&logo=tailwindcss&logoColor=black" />
<img alt="Express" src="https://img.shields.io/badge/express-404040?style=flat-square&labelColor=0d1117&logo=express&logoColor=white" />
<img alt="PostgreSQL" src="https://img.shields.io/badge/postgresql-4169E1?style=flat-square&labelColor=0d1117&logo=postgresql&logoColor=white" />
<img alt="Docker" src="https://img.shields.io/badge/docker-2496ED?style=flat-square&labelColor=0d1117&logo=docker&logoColor=white" />
</p>

<p><sub>Professional work — private repository.</sub></p>

<h3>SVSP policy &amp; impact portal</h3>

Multi-language member portal for a policy organisation: membership payments,
encrypted document handling, receipt and PDF generation, analytics dashboards and
a full OpenAPI contract.

<p>
<img alt="React" src="https://img.shields.io/badge/react-61DAFB?style=flat-square&labelColor=0d1117&logo=react&logoColor=black" />
<img alt="Vite" src="https://img.shields.io/badge/vite-646cff?style=flat-square&labelColor=0d1117&logo=vite&logoColor=white" />
<img alt="Tailwind" src="https://img.shields.io/badge/tailwind-38BDF8?style=flat-square&labelColor=0d1117&logo=tailwindcss&logoColor=black" />
<img alt="Razorpay" src="https://img.shields.io/badge/razorpay-22c1c3?style=flat-square&labelColor=0d1117" />
<img alt="pdf-lib" src="https://img.shields.io/badge/pdf--lib-6ce5a8?style=flat-square&labelColor=0d1117" />
<img alt="i18next" src="https://img.shields.io/badge/i18next-38bdf8?style=flat-square&labelColor=0d1117" />
</p>

<p>
<a href="https://github.com/bilwg-services/swadeshi-vitta-salahakar-parishad"><img alt="SVSP portal source" src="https://img.shields.io/badge/github-1e1e1e?style=for-the-badge&logo=github&logoColor=white" /></a>
</p>

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">

<h3>Tenant storefront engine</h3>

Multi-tenant storefront toolkit with a DSL verifier, JWT auth and Redis caching —
plus a small <b>island-hydration SSR framework</b> I wrote to keep client JS small.

<p>
<img alt="Express" src="https://img.shields.io/badge/express-404040?style=flat-square&labelColor=0d1117&logo=express&logoColor=white" />
<img alt="EJS" src="https://img.shields.io/badge/ejs-a91e50?style=flat-square&labelColor=0d1117" />
<img alt="Redis" src="https://img.shields.io/badge/redis-dc382d?style=flat-square&labelColor=0d1117&logo=redis&logoColor=white" />
<img alt="SQLite" src="https://img.shields.io/badge/sqlite-0b80d3?style=flat-square&labelColor=0d1117&logo=sqlite&logoColor=white" />
</p>

<h3>SreeIyer e-commerce platform</h3>

Storefront and admin for a digital commerce platform: Stripe checkout, realtime
order socket, cloud object storage, ebook and document processing pipeline.

<p>
<img alt="Next.js" src="https://img.shields.io/badge/next.js-e9e9e9?style=flat-square&labelColor=0d1117" />
<img alt="React" src="https://img.shields.io/badge/react-61DAFB?style=flat-square&labelColor=0d1117&logo=react&logoColor=black" />
<img alt="Stripe" src="https://img.shields.io/badge/stripe-635bff?style=flat-square&labelColor=0d1117&logo=stripe&logoColor=white" />
<img alt="MongoDB" src="https://img.shields.io/badge/mongodb-4db33d?style=flat-square&labelColor=0d1117&logo=mongodb&logoColor=white" />
<img alt="Socket.IO" src="https://img.shields.io/badge/socket.io-010101?style=flat-square&labelColor=0d1117&logo=socketdotio&logoColor=white" />
</p>

</td>
<td width="50%" valign="top">

<h3>LineageOS 21 custom kernel</h3>

Custom kernel 4.14.336 with KernelSU modifications, built and flashed for the
Poco M2 Pro — a reminder that not every bug lives in TypeScript.

<p>
<img alt="C" src="https://img.shields.io/badge/c-a8b9cf?style=flat-square&labelColor=0d1117" />
<img alt="Linux" src="https://img.shields.io/badge/linux-FCC624?style=flat-square&labelColor=0d1117&logo=linux&logoColor=black" />
<img alt="KernelSU" src="https://img.shields.io/badge/kernelsu-34d399?style=flat-square&labelColor=0d1117" />
</p>

<p>
<a href="https://github.com/its-skark/kernal_lineageos21.0_pocoM2pro"><img alt="Kernel source" src="https://img.shields.io/badge/source-1e1e1e?style=for-the-badge&logo=github&logoColor=white" /></a>
</p>

<h3>Tools &amp; experiments</h3>

<b>LucarioBot</b> — alert bot for Discord (Hikari). <b>LeadsGenerator</b> —
Python scraping utilities. <b>voxelEngine</b>, <b>router-cli</b> (Go) and
<b>LinuxSyncVolume</b> shell automation, plus a personal site and a remote-meeting UI.

<p>
<img alt="Python" src="https://img.shields.io/badge/python-3776AB?style=flat-square&labelColor=0d1117&logo=python&logoColor=white" />
<img alt="Go" src="https://img.shields.io/badge/go-00add8?style=flat-square&labelColor=0d1117&logo=go&logoColor=white" />
<img alt="Shell" src="https://img.shields.io/badge/shell-4eaa25?style=flat-square&labelColor=0d1117" />
<img alt="PHP" src="https://img.shields.io/badge/php-777bb4?style=flat-square&labelColor=0d1117&logo=php&logoColor=white" />
</p>

<p><a href="https://github.com/its-skark?tab=repositories">see all repositories →</a></p>

</td>
</tr>
</table>

<img src="assets/divider.svg" width="100%" alt="decorative divider" />

## Experience

<table>
<tr>
<td valign="top" width="24%"><b>Bilwg Services Pvt. Ltd.</b><br /><sub>May 2026 → Present · Remote</sub></td>
<td valign="top">
<b>Software Developer</b> — full-stack product engineering
<ul>
<li>Building and maintaining <b>Angular</b> front-end features for client-facing SaaS products, pairing with senior engineers on feature design and delivery.</li>
<li>Implementing <b>full-stack features in React and Express</b> across REST APIs, auth and data layers used by real customers.</li>
<li>Contributing to code reviews, debugging, testing and deployments.</li>
</ul>
</td>
</tr>
<tr>
<td valign="top"><b>Delosch Technologies Pvt. Ltd.</b><br /><sub>Jun 2025 → Aug 2025 · Hybrid</sub></td>
<td valign="top">
<b>Full-Stack &amp; AI Engineering Intern</b>
<ul>
<li><b>AI automation:</b> engineered custom contexts and tuned prompt designs on <b>AWS Bedrock</b> to automate HR workflows and cut manual processing.</li>
<li><b>Full-stack:</b> shipped responsive Remix.js + React surfaces focused on cross-device performance.</li>
<li><b>Cloud:</b> integrated <b>S3</b> for scalable file storage and <b>DynamoDB</b> for high-performance NoSQL access.</li>
<li><b>DevOps:</b> stood up <b>EC2</b> instances, backend services and <b>Nginx reverse proxies</b>.</li>
</ul>
</td>
</tr>
<tr>
<td valign="top"><b>SCPPS</b><br /><sub>2022 → 2024 · Pantnagar</sub></td>
<td valign="top">
<b>Technical Committee Lead</b>
<ul>
<li>Architected and deployed the society's official blog and digital infrastructure.</li>
<li>Led a cross-functional team running web infrastructure for events with <b>500+ attendees</b>.</li>
<li>Set up the society's payments, member portal and document tooling.</li>
</ul>
</td>
</tr>
</table>

<img src="assets/divider.svg" width="100%" alt="decorative divider" />

## Education

**B.Tech, Information Technology** — Govind Ballabh Pant University of Agriculture and Technology, 2022 → 2026

<sub>Graduated June 2026. SkillFlow, above, was my major final-year project.</sub>

**XII (ISC)** — St. Mary's Convent Inter College, 2022

## GitHub activity

<p align="center">
  <img src="assets/snake.svg?v=1f025de" width="100%" alt="Contribution graph — the snake eats through the year" />
</p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=its-skark&amp;show_icons=true&amp;include_all_commits=true&amp;hide_border=true&amp;theme=github_dark&amp;border_color=21262d" alt="Rachit Pandey's GitHub stats" width="330" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs?username=its-skark&amp;layout=compact&amp;hide_border=true&amp;theme=github_dark&amp;border_color=21262d" alt="Top languages by public repo bytes" width="270" />
  <img src="https://streak-stats.demolab.com/?user=its-skark&amp;theme=github_dark&amp;hide_border=true" alt="GitHub contribution streak" width="330" />
</p>

<details>
<summary><b>Notes on the stats above</b></summary>

- <b>Top languages</b> counts only <i>public</i> repository bytes. Most of my professional TypeScript/Angular/Express work lives in private repositories at my employer, so it understates TypeScript badly. The stack cards above are the accurate picture.
- The repo count and follower badges are live queries. shields.io's `github/repos`, `/contributors` and `/last-commit` endpoints are currently returning "badge not found" for every user, so those three were replaced with values verified against the API.
- The stats, streak and snake images are the only parts that depend on something outside this repository. Every other visual is a self-hosted SVG in `assets/`, so if those fail the page still looks finished.

</details>

## Let's connect

<p align="center">
  <a href="https://github.com/its-skark"><img src="https://img.shields.io/badge/github-8b5cf6?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://twitter.com/rachitp04"><img src="https://img.shields.io/badge/twitter-22d3ee?style=for-the-badge&logo=x&logoColor=black" alt="X" /></a>
  <a href="https://itsrachit.qzz.io/"><img src="https://img.shields.io/badge/portfolio-34d399?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>
  <a href="mailto:rachit_pandey2004@outlook.com"><img src="https://img.shields.io/badge/email-fbbf24?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
</p>

<p align="center">
  Open to <b>full-stack</b>, <b>product</b> and <b>AI engineering</b> roles —
  and always happy to talk architecture, POS systems, code intelligence or
  custom kernels.
</p>

<p align="center">
  <img src="assets/divider.svg" width="70%" alt="decorative divider" />
</p>

<p align="center">
  <sub>Designed and built with HTML, CSS and stubborn curiosity ·
  <a href="https://github.com/its-skark/its-skark">source on GitHub</a></sub>
</p>
