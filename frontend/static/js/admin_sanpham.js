const API = "http://127.0.0.1:8000";

// --------------------- OPEN CREATE ---------------------
function openCreate() {
    new bootstrap.Modal("#modalCreateSP").show();
}

// --------------------- CREATE ---------------------
async function createSP() {
    let ten = document.getElementById("c_ten").value;
    let mota = document.getElementById("c_mota").value;
    let file = document.getElementById("c_anh").files[0];

    if (!ten) return Swal.fire("Thiếu tên sản phẩm!", "", "warning");

    // Upload ảnh
    let anh_url = "";
    if (file) {
        const form = new FormData();
        form.append("file", file);

        let res = await fetch(`${API}/sanpham/upload-image`, {
            method: "POST",
            body: form
        });

        anh_url = (await res.json()).url;
    }

    await fetch(`${API}/sanpham/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            tensanpham: ten,
            mota: mota,
            anh: anh_url
        })
    });

    Swal.fire("Đã thêm!", "", "success").then(() => location.reload());
}

// --------------------- OPEN EDIT ---------------------
function openEdit(id, ten, mota) {
    document.getElementById("e_id").value = id;
    document.getElementById("e_ten").value = ten;
    document.getElementById("e_mota").value = mota;

    new bootstrap.Modal("#modalEditSP").show();
}

// --------------------- UPDATE ---------------------
async function updateSP() {
    let id = document.getElementById("e_id").value;
    let ten = document.getElementById("e_ten").value;
    let mota = document.getElementById("e_mota").value;
    let file = document.getElementById("e_anh").files[0];

    let anh_url = null;

    // Nếu có upload ảnh mới → gửi API upload
    if (file) {
        const form = new FormData();
        form.append("file", file);

        let res = await fetch(`${API}/sanpham/upload-image`, {
            method: "POST",
            body: form
        });

        anh_url = (await res.json()).url;
    }

    await fetch(`${API}/sanpham/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            tensanpham: ten,
            mota: mota,
            anh: anh_url  // nếu null → backend tự giữ ảnh cũ
        })
    });

    Swal.fire("Đã cập nhật!", "", "success").then(() => location.reload());
}

// --------------------- DELETE ---------------------
async function deleteSP(id) {
    Swal.fire({
        title: "Xóa sản phẩm?",
        icon: "warning",
        showCancelButton: true,
    }).then(async (r) => {
        if (r.isConfirmed) {
            await fetch(`${API}/sanpham/${id}`, { method: "DELETE" });
            Swal.fire("Đã xóa!", "", "success")
                .then(() => location.reload());
        }
    });
}
