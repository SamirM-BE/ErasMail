module.exports = {
    devServer: {
        proxy: {
            '^/api/': {
                target: 'web:8000',
            }
        }
    },
}