workflow "New workflow" {
  on = "push"
  resolves = ["daysm/bsp-actions/make-pdfs@master"]
}

action "Make song sheet PDFs" {
  uses = "daysm/bsp-actions/make-pdfs@master"
  runs = "make"
}

action "daysm/bsp-actions/make-pdfs@master" {
  uses = "daysm/bsp-actions/make-pdfs@master"
  needs = ["Make song sheet PDFs"]
  runs = "make"
  args = "songbook"
}
