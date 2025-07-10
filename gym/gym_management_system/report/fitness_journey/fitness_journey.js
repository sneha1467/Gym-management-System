frappe.query_reports["Fitness Journey"] = {
    filters: [
        {
            fieldname: "member",
            label: "Gym Member",
            fieldtype: "Link",
            options: "Gym Membership",
            reqd: 1
        }
    ]
};
