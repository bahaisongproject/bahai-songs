workflow "New workflow" {
  on = "push"
  resolves = ["Make PDFs"]
}

action "Make PDFs" {
  uses = "daysm/bsp-actions/make-pdfs@044faeb"
}
