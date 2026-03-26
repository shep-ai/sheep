# Offline Markdown Content

Offline generation keeps tests deterministic when no external API keys are available in the current environment, and it still produces coherent markdown that looks like real output. The formatter ensures there is an H1 heading, a blank separator line, and then exactly a few sentences of prose that end cleanly with periods. With this fallback, validation can focus on structure rather than network access or provider configuration, so the suite remains stable.
