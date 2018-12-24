workflow "Make files" {
  on = "push"
  resolves = [
    "List files"
  ]
}

action "Make song sheet PDFs" {
  uses = "daysm/bsp-actions/make-pdfs@master"
  runs = "make"
}

action "Make song book PDF" {
  uses = "daysm/bsp-actions/make-pdfs@master"
  runs = "make"
  args = "songbook"
}

action "List files" {
  uses = "daysm/bsp-actions/publish-pdfs@master"
  needs = ["Make song sheet PDFs", "Make song book PDF"]
  runs = "find"
  args = "bahai-songs -maxdepth 2"
}
