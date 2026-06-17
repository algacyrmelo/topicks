# topicks

Tool that saves your time deciding what to study next.

> I made it specially for public service exams
> with lots of subjects and topics.

## Usage

```bash
python3 main.py topics.csv # Pick a topic
python3 main.py topics.csv [--done] # Register you're done with current topic
```

## TO DO

- [x] Toggle current topic by putting/removing a '*' mark on *current* field
- [x] Update review cycle when current topic is done
- [x] Handle never studied topics
- [ ] Improve user feedback and error handling
- [ ] Evaluate the topic score system's balance
- [ ] Refactor code

## Future Enhancements

- Add subject weight/number of questions to the score calculation
- Generate a proper CSV programmatically
