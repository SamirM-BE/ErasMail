const units = ['B', 'kB', 'MB', 'GB', 'TB']

function log(x, y) {
    return Math.log(x) / Math.log(y);
}

function convert_size(size_bytes) {
    if (!size_bytes) {
        return '0 B'
    }
    let order_of_magnitude = Math.floor(log(size_bytes, 1024))
    let p = 1024 ** order_of_magnitude
    let size = Math.round(size_bytes / p, 2)
    return `${size} ${units[order_of_magnitude]}`
}


export {
    convert_size
}