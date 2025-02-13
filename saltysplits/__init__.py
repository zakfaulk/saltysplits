DATETIME_FORMAT = r"%m/%d/%Y %H:%M:%S"
NANOSECONDS_DAY = 86400 * 10**9
NANOSECONDS_HOUR = 3600 * 10**9
NANOSECONDS_MINUTE = 60 * 10**9
NANOSECONDS_SECOND = 10**9

# OUTLINE of LSS structure based on THUG1/VC/RE2
# Run
    # GameIcon
    # GameName
    # CategoryName
    # LayoutPath
    # Metadata
        # Run
        # Platform
        # Region
        # Variables
            # Variable
    # Offset
    # AttemptCount
    # AttemptHistory
        # Attempt
            # RealTime 
            # GameTime
    # Segments
        # Segment
            # Name
            # Icon
            # Split Times
                # Split Time
                    # RealTime
                    # GameTime
            # Best Segment Time
                # RealTime
                # GameTime
            # SegmentHistory
                # Time
                    # RealTime
                    # GameTime
    # AutoSplitterSettings
        # Version
        # CustomSettings

