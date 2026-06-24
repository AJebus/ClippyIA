# ClippyIA
Build an AI Agent:  We're building a toy version of Claude Code using Google's Gemini API!

What Does the Agent Do?

The program we're building is a CLI tool that:

    Accepts a coding task (e.g., "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽")
    Chooses from a set of predefined functions to work on the task, for example:
        Scan the files in a directory
        Read a file's contents
        Overwrite a file's contents
        Execute the Python interpreter on a file
    Repeats step 2 until the task is complete (or it fails miserably, which is possible)
