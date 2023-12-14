# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 12/13/2023
### General
- "find" and "update" methods should now work.
- "list" methods now return a dictionary containing the ID and NAME instead of a partial class. You will have to use "get" methods to convert them to classes

### Known Issues
- list_servers_by_connection, and update_server all throw "Access denied"
- get_own_api_key throws "Incorrect API key from user: USERNAME"

## [0.0.1] - 11/29/2023

Initial release