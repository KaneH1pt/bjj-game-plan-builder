# BJJ Game Plan Builder

A personal tool for mapping your Brazilian Jiu-Jitsu game as a directed graph — positions, transitions, and how they connect. Built as a portfolio project demonstrating that a domain-literate non-engineer can make rigorous architectural decisions and deliver a working product using AI as an engineering tool.

---

## Stack

React · FastAPI · PostgreSQL (Supabase) · Vercel · Railway

---

## Specification

The full product specification lives in `BJJ_Game_Tree_Specification.html`. It covers feature requirements in BDD scenario format, data models, security requirements, agent architecture, and the reasoning behind every significant design decision.

---

## How it's being built

This project is built using an AI agent pipeline operating within GitHub Actions. The product owner (Kane Hellewell) owns the specification. Agents own implementation — one feature at a time, in order: Authentication → Nodes → Connectors.

---

## Current status

- [x] Infrastructure provisioned (Supabase, Railway, Vercel, GitHub Secrets)
- [x] Product specification complete
- [x] Single-file MVP prototype — visual and behavioural reference
- [x] GitHub Actions workflows
- [ ] Feature: Authentication
- [ ] Feature: Nodes
- [ ] Feature: Connectors

---

*Co-authored with Claude (Anthropic).*
