Correlation

Affine and splice files created from correlating data between holes. The affine files provide shift information for each core in a hole to align it with other holes.  The splice files provide a continous set of core information by combining intervals from different holes. 

Affine tables

    Site: site number
    Hole: hole number
    Core: core number
    Type: type indicates the coring tool used to recover the core (typical types are F, H, R, X).
    Depth CSF-A (m): top of core depth from the LIMS sample registry at the original CSF-A depth scale.
    Depth CCSF (m): top of core depth at the CCSF alternate depth scale. Depth CCSF (m) = Depth CSF-A (m) + Cumulative offset (m)
    Cumulative offset (m): distance a core was shifted along the depth axis relative to the original CSF-A depth.
    Differential offset (m): distance a core was shifted along the depth axis relative to its depth after the next shallower core was shifted. This value, when viewed in context, is useful to detect unusual shifts that may indicate a correlation error or stratigraphic irregularity.
    Growth rate: growth rate = Depth CCSF (m) / Depth CSF-A (m); a measure of the degree of expansion in the recovered sediment section relative to the in-situ section.
    Shift type: recommended terms are: anchor, tie, set, and append. This is an optional comment.
    Data type used: recommended terms are analysis names or acronyms, such as NGR, MSL, RGB, etc. This is an optional comment.
    Quality comment: recommended comments are those pointing to problematic shifts based on less than ideal data. This is an optional comment.

Splice interval tables

    Interval: sequential numbering of splice intervals added by the database.
    Site: site number
    Hole: hole number
    Core: core number
    Type: type indicates the coring tool used to recover the core (typical types are F, H, R, X).
    Top section: section number of top and bottom of splice interval, respectively.
    Top offset (cm): offset of top of splice interval.
    Top depth CSF-A (m): CSF-A depth of top of splice interval.
    Top depth CCSF (m): CCSF depth of top of splice interval.
    Bottom section: section number of bottom of splice interval.
    Bottom offset (cm): offset of bottom of splice interval.
    Bottom depth CSF-A (m): CSF-A depth of bottom of splice interval.
    Top/Bottom depth CCSF (m): CCSF depth of bottom of splice interval.
    Splice type: recommended terms are: anchor, tie, set, and append. This is an optional comment.
    Data type used: recommended terms are analysis names or acronyms, such as NGR, MSL, RGB, etc. This is an optional comment.
    Quality comment: recommended comments are those pointing to problematic intervals based on less than ideal signal. This is an optional comment.