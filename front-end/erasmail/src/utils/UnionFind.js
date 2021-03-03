// https://algs4.cs.princeton.edu/15uf/WeightedQuickUnionPathCompressionUF.java.html
class UnionFind {
    constructor(n) {
        this.count = n
        this.parent = []
        this.name = {}
        this.size = []
        for (let i = 0; i < n; i++) {
            this.parent.push(i)
            this.size.push(1)
        }
    }

    count() {
        return this.count
    }

    validate(p) {
        let n = this.parent.length
        if (p < 0 || p >= n) {
            throw `index ${p} is not between 0 and ${n-1}`
        }
    }

    groupNumber(p) { // name
        if (this.name[p] !== undefined) {
            this.validate(this.name[p])
            return this.parent[this.name[p]]
        }
        return undefined
    }

    numberOfMembre(p) { // name
        if (this.name[p] !== undefined) {
            this.validate(this.name[p])
            let count = 0
            let n = this.parent.length
            for (let i = 0; i < n; i++) {
                if (this.parent[this.name[p]] == this.parent[i]) {
                    count++
                }
            }
            return count
        }
        return undefined
    }

    find(p) {

        this.validate(p)
        let root = p
        while (root !== this.parent[root])
            root = this.parent[root]

        while (p !== root) {
            let newp = this.parent[p]
            this.parent[p] = root
            p = newp
        }
        return root
    }

    connected(p, q) {
        return this.find(this.name[p]) == this.find(this.name[q])
    }

    union(p, q) {
        this.name[p.name] = p.idx
        this.name[q.name] = q.idx
        let rootP = this.find(p.idx)
        let rootQ = this.find(q.idx)

        if (rootP === rootQ) return

        // make smaller root point to larger one
        if (this.size[rootP] < this.size[rootQ]) {
            this.parent[rootP] = rootQ
            this.size[rootQ] += this.size[rootP]
        } else {
            this.parent[rootQ] = rootP
            this.size[rootP] += this.size[rootQ]
        }
        this.count--
    }
}

export {
    UnionFind
}