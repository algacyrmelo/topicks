# Topicks

This tool picks a study topic from a CSV file based on priority parameters.

## Requirements

- Read a list of topics from a CSV file
- Pick a topic suggestion for the user to study
- Update and save the progress

## Usage
`python3 main.py topics.csv [--done]`

## TODO

- [x]Mark a topic as *picked*, enabling the user to mark as *done*
- [ ]Update the review cycle by the time a topic is done

## Problems

- How the user is going to mark a topic as studied?

    Via CLI arguments. (pick, done...)

- Should I need unique ID's to the subjects or topics?

## Future Enhancements

- Get topics and other kind of data directly from public notice and exam's PDF
