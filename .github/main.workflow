workflow "Make PDFs" {
  on = "push"
  resolves = [
    "Make song sheet PDFs",
    "new-action",
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

action "List PDFs" {
  uses = "daysm/bsp-actions/publish-pdfs@master"
  needs = ["Make song sheet PDFs", "Make song book PDF"]
  runs = "find"
  args = "bahai-songs -maxdepth 2"
}
