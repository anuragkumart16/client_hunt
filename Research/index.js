(async function hehe() {
    const response = await fetch('https://www.fit-nest.in/api/Admin/AllMembershipPlans')
    const data = await response.json()
    console.log(data)
})()

