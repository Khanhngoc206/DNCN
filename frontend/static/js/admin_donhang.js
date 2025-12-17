const API = "http://127.0.0.1:8000";


// ======================
// XEM CHI TIẾT ĐƠN HÀNG
// ======================
async function viewDetail(id) {

    let res = await fetch(`${API}/donhang/${id}`);
    let dh = await res.json();

    let html = `
        <h5>Khách hàng: ${dh.tenkh}</h5>
        <p>Ngày lập: ${dh.ngaylap}</p>
        <p>Trạng thái: <b>${dh.trangthai}</b></p>
        <h5 class="mt-3">Chi tiết sản phẩm</h5>
        <table class="table table-bordered">
            <tr>
                <th>Sản phẩm</th><th>Size</th><th>SL</th><th>Giá</th>
            </tr>
    `;

    dh.chitiet.forEach(ct => {
        html += `
            <tr>
                <td>${ct.tensanpham}</td>
                <td>${ct.tensize}</td>
                <td>${ct.soluong}</td>
                <td>${ct.gia} đ</td>
            </tr>
        `;
    });

    html += "</table>";

    document.getElementById("detailContent").innerHTML = html;

    new bootstrap.Modal("#modalDetail").show();
}



// ======================
// CẬP NHẬT TRẠNG THÁI
// ======================

function openUpdateStatus(id, cur) {
    document.getElementById("st_id").value = id;
    document.getElementById("st_value").value = cur;
    new bootstrap.Modal("#modalStatus").show();
}


async function updateStatus() {
    let id = document.getElementById("st_id").value;
    let st = document.getElementById("st_value").value;

    await fetch(`${API}/donhang/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trangthai: st })
    });

    Swal.fire("Đã cập nhật!", "", "success")
        .then(() => location.reload());
}



// ======================
// XÓA ĐƠN HÀNG
// ======================

async function deleteOrder(id) {

    Swal.fire({
        title: "Xóa đơn hàng?",
        icon: "warning",
        showCancelButton: true
    }).then(async (result) => {

        if (result.isConfirmed) {

            await fetch(`${API}/donhang/${id}`, { method: "DELETE" });

            Swal.fire("Đã xóa!", "", "success")
                .then(() => location.reload());
        }
    });
}
