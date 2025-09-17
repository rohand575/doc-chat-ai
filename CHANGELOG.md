# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-09-17
### Added
- Progress bar during PDF processing.
- Document statistics (pages, words, chunks) in sidebar.
- Clear chat history button.
- Download chat history button.
- Multiple PDF upload support (up to 5 files, 10MB each).
- Minimalistic, professional UI styling with custom CSS.

### Changed
- Sidebar layout for upload, stats, and actions.
- Chat history displayed latest-first.
- Removed LangChain chat memory to prevent format errors.

### Fixed
- KeyError for missing document stats.
- AttributeError with `st.experimental_rerun()` updated to `st.rerun()`.
- Chat errors due to unsupported chat history format.

## [1.1.0] - YYYY-MM-DD
### Added
- Initial chat history functionality.
- Basic PDF processing and vector store setup.

### Fixed
- Basic bug fixes from v1.0.0.

## [1.0.0] - YYYY-MM-DD
### Initial Release
- Upload PDF and ask questions.
- Basic Q&A with OpenAI embeddings and FAISS.
