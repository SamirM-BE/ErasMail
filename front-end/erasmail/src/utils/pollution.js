function pollutionCompare(item, emailCO2){
    return  Math.round(emailCO2 / item)
}

const comparison = {
    paperCup: (emailCO2) => {
        let cmp = pollutionCompare(2.8, emailCO2)
        return {
            value: cmp, // https://www.huhtamaki.com/en/highlights/sustainability/taking-a-closer-look-at-the-carbon-footprint-of-paper-cups-for-coffee/
            msg: `${cmp} paper cup(s)`,
            level: 1,
        }
    } , 
    plasticBag: (emailCO2) => {
        let cmp = pollutionCompare(10, emailCO2)
        return {
            value: cmp, // banana
            msg: `manufacturing ${cmp} plastic bag(s)`,
            level: 2,
        }
    }, 
    tv: (emailCO2) => {
        let cmp = pollutionCompare(40, emailCO2)
        return {
            value: cmp,  // bananas (during 1 hour)
            msg: `watching TV during ${cmp} hour(s)`,
            level: 3,
        }
    }, 
    car: (emailCO2) => {
        let cmp =  pollutionCompare(126, emailCO2) 
        return {
            value: cmp,  // https://ecoscore.be/fr/info/ecoscore/co2?path=info%2Fecoscore%2Fco2 moyenne entre essence et diesel (for 1 km)
            msg: `driving a car for ${cmp} km`,
            level: 4,
        }
    },
}

function getAllComparisons(emailCO2){
    
    let comparisons = new Array()
    let level = 0

    for (const property in comparison) {
        let cmp = comparison[property](emailCO2)
        if(cmp.value){
            comparisons.push({
                name: property,
                ...cmp
            })
            if(cmp.level > level){
                level = cmp.level
            }
        }
    }

    comparisons.sort((a, b) => a.level - b.level)
    return {comparisons, level}
}


function getOptimalComparison(emailCO2){
    let name = ''
    let value = Number.POSITIVE_INFINITY
    let msg = ''
    let level = 0

    for (const property in comparison) {
        let cmp = comparison[property](emailCO2)
        if(cmp.value &&  cmp.value < value){
            name = property
            value = cmp.value
            msg = cmp.msg
            level = cmp.level
        }
    }
    if(name){
        return {comparison:{name, value, msg}, level}
    }
    return {level}
}

export {
    getAllComparisons,
    getOptimalComparison
}