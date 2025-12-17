const API = "http://127.0.0.1:8000";

// ========================
// OPEN CREATE MODAL
// ========================
function openCreatePB() {
    new bootstrap.Modal("#modalCreatePB").show();
}

// ========================
// CREATE
// ========================
async function createPB() {
    let sp = document.getElementById("c_sp").value;
    let mausac = document.getElementById("c_mausac").value;
    let gia = document.getElementById("c_gia").value;

    if (!mausac || !gia) 
        return Swal.fire("Thiếu dữ liệu!", "", "warning");

    await fetch(`${API}/phienban/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            masanpham: parseInt(sp),
            mausac: mausac,
            gia: parseInt(gia)
        })
    });

    Swal.fire("Thêm thành công!", "", "success")
        .then(() => location.reload());
}

// ========================
// OPEN EDIT MODAL
// ========================
function openEditPB(id, sp, mausac, gia) {

    document.getElementById("e_id").value = id;
    document.getElementById("e_sp").value = sp;
    document.getElementById("e_mausac").value = mausac;
    document.getElementById("e_gia").value = gia;

    new bootstrap.Modal("#modalEditPB").show();
}

// ========================
// UPDATE
// ========================
async function updatePB() {
    let id = document.getElementById("e_id").value;
    let sp = document.getElementById("e_sp").value;
    let mausac = document.getElementById("e_mausac").value;
    let gia = document.getElementById("e_gia").value;

    await fetch(`${API}/phienban/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            masanpham: parseInt(sp),
            mausac: mausac,
            gia: parseInt(gia)
        })
    });

    Swal.fire("Cập nhật thành công!", "", "success")
        .then(() => location.reload());
}

// ========================
// DELETE
// ========================
async function deletePB(id) {
    Swal.fire({
        title: "Xóa phiên bản?",
        icon: "warning",
        showCancelButton: true,
    }).then(async (r) => {
        if (r.isConfirmed) {
            await fetch(`${API}/phienban/${id}`, { method: "DELETE" });
            Swal.fire("Đã xóa!", "", "success")
                .then(() => location.reload());
        }
    });
}
