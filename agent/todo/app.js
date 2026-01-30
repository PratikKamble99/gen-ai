const STORAGE_KEY = "todo.items.v1";
let items = load();
let filter = "all";

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");
const counter = document.getElementById("counter");
const clearCompletedBtn = document.getElementById("clear-completed");
const filterBtns = Array.from(document.querySelectorAll(".chip[data-filter]"));

render();

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const title = input.value.trim();
    if (!title) return;
    items.unshift({
        id: String(Date.now() + Math.random()),
        title,
        done: false,
    });
    input.value = "";
    save();
    render();
});

clearCompletedBtn.addEventListener("click", () => {
    items = items.filter((t) => !t.done);
    save();
    render();
});

filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        filter = btn.dataset.filter;
        filterBtns.forEach((b) => b.classList.toggle("active", b === btn));
        render();
    });
});

function getVisibleItems() {
    if (filter === "active") return items.filter((t) => !t.done);
    if (filter === "completed") return items.filter((t) => t.done);
    return items;
}

function render() {
    const visible = getVisibleItems();
    list.innerHTML = "";

    visible.forEach((t) => {
        const li = document.createElement("li");
        li.className = "item" + (t.done ? " completed" : "");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "check";
        checkbox.checked = t.done;
        checkbox.addEventListener("change", () => {
            t.done = !t.done;
            save();
            render();
        });

        const title = document.createElement("div");
        title.className = "title";
        title.textContent = t.title;

        const del = document.createElement("button");
        del.className = "icon-btn";
        del.type = "button";
        del.textContent = "✕";
        del.addEventListener("click", () => {
            items = items.filter((x) => x !== t);
            save();
            render();
        });

        li.appendChild(checkbox);
        li.appendChild(title);
        li.appendChild(del);
        list.appendChild(li);
    });

    const activeCount = items.filter((t) => !t.done).length;
    counter.textContent = `${activeCount} item${activeCount === 1 ? "" : "s"} left`;
    clearCompletedBtn.disabled = items.every((t) => !t.done);
}

function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function load() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch {}
}
