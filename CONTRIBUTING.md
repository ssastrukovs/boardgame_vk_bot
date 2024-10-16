# How to make the bot better

## Contributing

For now, either:
1. Start an issue with what is urgent to be done 
2. Open a pull request, if you're willing to do something yourself.

Pull requests are prefferable.

    
## Code style, comments, commits messages etc.

Try to keep it simple and not overpollute it with comments.

As for the **commit** policy, start a new branch with your feature, and keep to the simple generic rules when naming:
1. Verb at the start of commit header, as in "this commit will ..."
2. 50 symbols in commit header and 72 in commit message line max
3. An empty new line that separates the header and message
4. Name your branches in underscore case

Also, there's a little CI script that does linting after submitting a PR.    
Maybe run pylint like that, it does exactly that:
```
pylint $(git ls-files '*.py')
```

Python version 3.9 is in there, so beware of using new features, or contact me to change it,
if it's a very unique new feature that NEEDS to be embedded in the repository.

For formatting, just run [ruff](https://github.com/astral-sh/ruff) with standard settings over it, and go with the pylint script I've given earlier from there.

## Language

Try to keep everything in English, where it's possible. Commit names must be **strictly** English

As for the code, try to keep everything in Python and shell scripting, be it bash/powershell/etc.

## Tests

**WIP**, but maybe test on your own VK group manually for now.

If someone's willing to add a unit-test & CI/CD frameworks/integrations, I will be very grateful.