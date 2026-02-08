--language, -l LANG  # Force language (python|node|bash|ruby|go)
--args "ARGS"        # Arguments to pass to script
--env KEY=VALUE, -e  # Environment variables (multiple)
--env-file FILE      # Load env vars from file
--profile <name>     # Security profile (strict|moderate|permissive|custom)
--timeout <sec>      # Kill execution after N seconds
--network NETWORK    # Network mode (none|bridge|host)
--memory, -m SIZE    # Memory limit (512m, 1g, etc)
--cpus NUM           # CPU limit (0.5, 1.0, 2.0)
--disk-size SIZE     # Disk space limit
--pids-limit NUM     # Max number of processes
--image IMAGE        # Use specific Docker image
--dockerfile FILE    # Build from custom Dockerfile
--platform PLATFORM  # Set platform (linux/amd64, linux/arm64)
--pull               # Always pull latest image
--no-cache           # Don't use Docker cache
--rm                 # Remove container after run (default: true)
--keep               # Keep container after execution
safebox profile list                  # List available profiles
safebox profile show PROFILE          # Show profile details
safebox profile create NAME           # Create custom profile
safebox profile edit NAME             # Edit profile
safebox profile delete NAME           # Delete profile
safebox profile export NAME           # Export profile to YAML
safebox profile import FILE           # Import profile from YAML