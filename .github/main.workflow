workflow "New workflow" {
  on = "push"
  resolves = ["Make PDFs"]
}

action "Make PDFs" {
  uses = "daysm/bsp-actions/make-pdfs@d10c452"
}
