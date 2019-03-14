function openArchiveNav() {
    document.getElementById("archive-nav").style.width = "320px";
/*     document.getElementById("main").style.paddingRight = "320px"; */
}

function closeArchiveNav() {
    document.getElementById("archive-nav").style.width = "0";
/*     document.getElementById("main").style.paddingRight = "0"; */
}

function openTagNav() {
    document.getElementById("tag-nav").style.width = "320px";
/*     document.getElementById("main").style.paddingRight = "320px"; */
}

function closeTagNav() {
    document.getElementById("tag-nav").style.width = "0";
/*     document.getElementById("main").style.paddingRight = "0"; */
}

$(document).ready(() => {
    $(".navbar").hover(
        () => {
            $(".navbar-brand-short").fadeOut("slow", () => {
            });
            $(".navbar-brand-full").fadeIn("slow", () => {
            });
        },
        () => {
            $(".navbar-brand-short").fadeIn("slow", () => {
            });
            $(".navbar-brand-full").fadeOut("slow", () => {
            });
        }
    );
});