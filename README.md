# Topicks

This tool picks a study topic from a CSV file based on priority parameters.

## Requirements

- Read a CSV file with subjects and topics data
- Pick a topic suggestion for the user to study
- Update and save the progress

## Data Model

- Topic: name, last_studied, category[general, specialized]

## Logic

```
read topics from CSV file
pick a topic based on:
    last_studied, spaced_review, number of questions,
    exam_phase(pre/pos-notice)
```

## Problems

- How the user is going to mark a topic as studied?
- Maybe should give unique ID's to the topics

## Future Enhancements

- Get data directly from public notice and exam's PDF
