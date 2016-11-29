class: Workflow
cwlVersion: v1.0
inputs:
  dir_in: Directory
outputs:
  saf:
    outputSource: frog-to-saf/saf
    type:
      items: File
      type: array
steps:
  frog-dir:
    in:
      dir_in: dir_in
    out:
    - frogout
    run: frog-dir.cwl
  frog-to-saf:
    in:
      in_files: frog-dir/frogout
    out:
    - saf
    run: frog-to-saf.cwl
