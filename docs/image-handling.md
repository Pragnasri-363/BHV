# Image Handling (Proposed):

This document describes a minimal and privacy-preserving image upload and storage pipeline for BHV.Since the backend is currently not implemented, this document serves as a design reference for future work.

## Goals

- Preserve user privacy
- Avoid unnecessary system complexity
- Keep implementation minimal and auditable

## Proposed Image Upload Flow

1. User uploads an image via the web interface
2. Server validates:
   - File type (image only)
   - File size (configurable limit)
3. Image metadata (EXIF) is stripped
4. Sanitized image is stored on disk
5. An index entry is created for retrieval

## Why Strip EXIF Metadata

Images may contain embedded metadata such as:

- GPS location
- Device identifiers
- Timestamps

Retaining this metadata may unintentionally expose sensitive user information. For a behavioral health application, this poses a significant risk to user privacy. Therefore, all metadata will be removed prior to storage.

## Implementation Notes (Future Work)

- EXIF stripping should occur server-side
- Original image bytes should not be persisted
- Visual image content must remain unchanged
- Processing should fail safely if metadata cannot be removed

## Non-Goals

- No client-side metadata processing
- No complex image transformations
- No automatic image analysis
