workflow "New workflow" {
  on = "push"
  resolves = ["Make PDFs"]
}

action "Make PDFs" {
  uses = "daysm/bsp-actions/make-pdfs@1d69c08"
  runs = "make"
}
