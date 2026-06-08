# Plug-and-Play Document Handler Library

A lightweight, local, and flexible document utility designed to strip away the overhead of manual data extraction, complex loops, and nested dictionaries. Whether you are building a custom LLM pipeline or just need quick, multi-format file parsing, this tool gives you instant access to your data.

---

## 🚀 The Motivation

When building custom AI orchestration workflows or experimenting with Retrieval-Augmented Generation (RAG) systems, managing file ingestion can quickly become overwhelming. 

This library was built to solve that exact problem. It acts as a dedicated component in your data pipeline, handling the heavy lifting of document parsing so you can focus entirely on your application's logic, agent routing, or prompt engineering.

---

## ✨ Features

* **Keyword Search:** Instantly query across all documents in your library.
* **Targeted Filtering:** Narrow down your searches by applying or resetting column/key filters on specific files.
* **Schema Discovery:** View the data layout and structure of your files programmatically without manually opening them.
* **Data Peeking:** Take a quick glance at the underlying content of single or multiple files.
* **Flexible Formatting:** Toggle search results to return as raw strings or Python dictionaries.

---

## 📂 Supported File Formats

The library is designed around a universal parsing framework with support for the following formats:

* [x] **JSONL** (Supported)
* [ ] **JSON** (Planned)
* [ ] **CSV** (Planned)
* [ ] **PDF** (Planned)

---

## 🛠️ Quick Start & Usage
View the demo_use.py file to check how to utilize the library to its max