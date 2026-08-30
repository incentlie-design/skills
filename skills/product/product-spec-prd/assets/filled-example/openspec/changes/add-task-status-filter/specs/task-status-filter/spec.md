## Purpose

Let local task-list users focus on a completion state, retain that choice in the current browser, and continue filtering when preference storage is unavailable.

## ADDED Requirements

### Requirement: Filter tasks by completion state

The system SHALL offer all, open and done filters, display only matching tasks in their existing order, and leave task data unchanged. This requirement maps to REQ-001 and AC-001.

#### Scenario: Select each status

- **GIVEN** t1 and t3 are open and t2 is done, ordered t1, t2, t3
- **WHEN** the user selects open, done, then all
- **THEN** the visible ids SHALL respectively be t1/t3, t2, and t1/t2/t3
- **AND** the source tasks and their order SHALL remain unchanged

### Requirement: Recover from an empty filtered result

The system SHALL distinguish no matching tasks from the unfiltered list and allow the user to clear the filter. This requirement maps to REQ-002 and AC-002.

#### Scenario: Empty result and clear

- **GIVEN** every existing task is done
- **WHEN** the user selects open
- **THEN** the system SHALL display “暂无未完成任务” and a clear-filter action
- **WHEN** the user clears the filter
- **THEN** selection SHALL become all and all existing tasks SHALL be visible
- **AND** if there are no tasks at all, the system SHALL display “暂无任务” while filters remain usable

### Requirement: Retain a usable local filter preference

The system SHALL persist a valid selection for the current browser when storage permits, restore it on reload, and default to all when no usable preference can be read. Storage errors SHALL NOT prevent current filtering. This requirement maps to REQ-003, AC-003 and AC-004.

#### Scenario: Storage write failure and recovery

- **GIVEN** preference writes fail
- **WHEN** the user selects done
- **THEN** done filtering SHALL take effect and “筛选偏好未保存” SHALL be visible
- **AND** the system SHALL NOT retry automatically
- **WHEN** storage recovers and the user explicitly selects open
- **THEN** open SHALL be saved and the previous error indicator SHALL be cleared

#### Scenario: Reload with valid or unusable preference

- **WHEN** the list reloads with the saved value done
- **THEN** done SHALL be selected and only completed tasks SHALL be displayed
- **WHEN** the saved value is absent or invalid
- **THEN** all SHALL be selected
- **WHEN** reading the preference throws an error
- **THEN** all SHALL be selected and “无法读取筛选偏好，已显示全部” SHALL be shown
- **AND** the user SHALL still be able to select another filter
