export function formatDate(value) {
    if (value === null || value === undefined) {
        return value;
    }

    if (typeof value !== "string") {
        return value;
    }

    const text = value.trim();
    if (!text) {
        return value;
    }

    const normalized = text.replace(" ", "T");
    const date = new Date(normalized);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day}-${month}-${year} -- ${hours}:${minutes}`;
}