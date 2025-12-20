# Tasks: Photo Album Organizer

**Input**: Design documents from `/specs/002-photo-album-organizer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are included as per the research document.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [ ] T002 Initialize Vite project in `frontend/`
- [ ] T003 [P] Configure linting and formatting tools for JavaScript
- [ ] T004 [P] Setup Vitest in `frontend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Setup SQLite database in `backend/src/database.js`
- [ ] T006 Create Album and Photo models in `backend/src/models.js`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Albums (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to create photo albums to organize my photos so that I can group related images together.

**Independent Test**: A user can create a new album and see it on the main page.

### Tests for User Story 1 ⚠️

**NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T007 [P] [US1] Write unit test for creating an album in `backend/tests/album.test.js`

### Implementation for User Story 1

- [ ] T008 [US1] Implement backend logic for creating an album in `backend/src/database.js`
- [ ] T009 [US1] Create a "Create Album" button in `frontend/src/main.js`
- [ ] T010 [US1] Implement frontend logic to call the backend and create an album in `frontend/src/main.js`
- [ ] T011 [US1] Display the newly created album on the main page in `frontend/src/main.js`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Organize Albums (Priority: P2)

**Goal**: As a user, I want to re-organize my albums by dragging and dropping them on the main page so that I can arrange them in a custom order.

**Independent Test**: A user can drag an album to a new position and the change is saved.

### Tests for User Story 2 ⚠️

- [ ] T012 [P] [US2] Write unit test for updating album order in `backend/tests/album.test.js`

### Implementation for User Story 2

- [ ] T013 [US2] Implement drag-and-drop functionality for albums in `frontend/src/main.js`
- [ ] T014 [US2] Implement backend logic to update the album order in `backend/src/database.js`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Photos in an Album (Priority: P3)

**Goal**: As a user, I want to see a tile-like preview of photos within an album so that I can quickly see the contents of the album.

**Independent Test**: A user can open an album and see the photos within it displayed as tiles.

### Tests for User Story 3 ⚠️

- [ ] T015 [P] [US3] Write unit test for fetching photos for an album in `backend/tests/photo.test.js`

### Implementation for User Story 3

- [ ] T016 [US3] Implement backend logic to fetch photos for a given album in `backend/src/database.js`
- [ ] T017 [US3] Implement frontend logic to display photos in a tile-like interface when an album is opened in `frontend/src/main.js`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T018 [P] Documentation updates in `docs/`
- [ ] T019 Code cleanup and refactoring
- [ ] T020 Performance optimization across all stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently
