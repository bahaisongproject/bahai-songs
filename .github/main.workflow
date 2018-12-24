workflow "Make PDFs" {
  on = "push"
  resolves = [
    "Make song sheet PDFs",
    "Make song book PDF",
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
