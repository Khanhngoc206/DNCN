const API = "http://127.0.0.1:8000";

// mở modal thêm
function openCreateSize() {
    new bootstrap.Modal("#modalCreateSize").show();
}

// thêm size
async function createSize() {

    let pb = document.getElementById("c_pb").value;
    let size = document.getElementById("c_size").value;
    let ton = document.getElementById("c_ton").value;

    await fetch(`${API}/size/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            maphienban: parseInt(pb),
            tensize: size,
            soluongton: parseInt(ton)
        })
    });

    Swal.fire("Đã thêm!", "", "success")
        .then(() => location.reload());
}


// mở modal sửa
function openEditSize(id, pb, size, ton) {

    document.getElementById("e_id").value = id;
    document.getElementById("e_pb").value = pb;
    document.getElementById("e_size").value = size;
    document.getElementById("e_ton").value = ton;

    new bootstrap.Modal("#modalEditSize").show();
}


// cập nhật size
async function updateSize() {

    let id = document.getElementById("e_id").value;
    let pb = document.getElementById("e_pb").value;
    let size = document.getElementById("e_size").value;
    let ton = document.getElementById("e_ton").value;

    await fetch(`${API}/size/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            maphienban: parseInt(pb),
            tensize: size,
            soluongton: parseInt(ton)
        })
    });

    Swal.fire("Đã cập nhật!", "", "success")
        .then(() => location.reload());
}


// xóa size
async function deleteSize(id) {

    Swal.fire({
        title: "Xóa size này?",
        icon: "warning",
        showCancelButton: true
    }).then(async (r) => {

        if (r.isConfirmed) {
            await fetch(`${API}/size/${id}`, {
                method: "DELETE"
            });

            Swal.fire("Đã xóa!", "", "success")
                .then(() => location.reload());
        }
    });
}
