document.addEventListener("DOMContentLoaded", function () {
  const giftForm = document.getElementById("giftForm");
  const successMessage = document.getElementById("successMessage");

  giftForm.addEventListener("submit", function (e) {
    e.preventDefault();

    // Lấy dữ liệu form
    const formData = {
      phone: document.getElementById("phone").value,
      name: document.getElementById("name").value,
    };

    // Kiểm tra validation
    if (!validateForm(formData)) {
      return;
    }

    // Hiển thị loading
    const submitBtn = document.querySelector(".gift-btn");
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = "⏳ Đang xử lý...";
    submitBtn.disabled = true;

    // Giả lập xử lý đăng ký
    setTimeout(() => {
      // Lưu thông tin người dùng (trong thực tế sẽ gửi lên server)
      localStorage.setItem("userInfo", JSON.stringify(formData));

      // Hiển thị thông báo thành công
      successMessage.style.display = "flex";

      // Reset form
      giftForm.reset();
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }, 2000);
  });
});

function validateForm(data) {
  // Kiểm tra số điện thoại
  const phoneRegex = /^[0-9]{10,11}$/;
  if (!phoneRegex.test(data.phone.replace(/\s/g, ""))) {
    showAlert("Vui lòng nhập số điện thoại hợp lệ (10-11 số)!");
    return false;
  }

  // Kiểm tra tên
  if (data.name.trim().length < 2) {
    showAlert("Vui lòng nhập họ tên hợp lệ!");
    return false;
  }

  return true;
}

function showAlert(message) {
  alert(message);
}

function showTerms() {
  const termsText = `
ĐIỀU KHOẢN VÀ ĐIỀU KIỆN CHƯƠNG TRÌNH QUÀ TẶNG

1. Chương trình chỉ áp dụng cho khách hàng mới đăng ký lần đầu.

2. Mỗi người chỉ được tham gia một lần duy nhất.

3. Thông tin cá nhân được bảo mật theo chính sách riêng tư.

4. Quà tặng sẽ được gửi qua email trong vòng 24 giờ.

5. Chương trình có thể kết thúc sớm nếu hết quà.

6. Mọi tranh chấp sẽ được giải quyết theo pháp luật Việt Nam.
    `;

  alert(termsText);
}

function downloadGift() {
  // Tải file Quà tặng.zip có sẵn
  const a = document.createElement("a");
  a.href = "Quà tặng.zip";
  a.download = "Quà tặng.zip";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  // Đóng popup sau 2 giây
  setTimeout(() => {
    successMessage.style.display = "none";
  }, 2000);
}

// Thêm hiệu ứng cho các phần tử khi cuộn
function animateOnScroll() {
  const elements = document.querySelectorAll(".gift-item");
  elements.forEach((el, index) => {
    setTimeout(() => {
      el.style.transform = "translateX(0)";
      el.style.opacity = "1";
    }, index * 200);
  });
}

// Gọi animation khi trang load
window.addEventListener("load", animateOnScroll);
