// main/static/js/app.js
document.addEventListener('DOMContentLoaded', () => {
  // --- ニックネーム（ひらがな・カタカナのみ） ---
  const nickname = document.querySelector('input[name="nickname"]');
  if (nickname) {
    let composing = false;

    const sanitizeKana = () => {
      // ひらがな・カタカナ・長音・濁点/半濁点・繰返し記号・中点のみ許可
      nickname.value = nickname.value.replace(/[^ぁ-んァ-ンー゛゜ヽヾ・]/g, '');
    };

    nickname.setAttribute('autocomplete', 'off');
    nickname.setAttribute('autocapitalize', 'off');

    nickname.addEventListener('compositionstart', () => { composing = true; });
    nickname.addEventListener('compositionend', () => { composing = false; sanitizeKana(); });
    nickname.addEventListener('input', (e) => { if (!e.isComposing && !composing) sanitizeKana(); });
  }

  // --- PIN入力（4桁を別inputで .pin-digit のとき）---
  const pinInputs = document.querySelectorAll('.pin-digit');
  // ここを両対応にする（どっちか見つかった方を使う）
  const hiddenPin = document.getElementById('password-hidden') || document.getElementById('birthday-hidden');

  if (pinInputs.length > 0 && hiddenPin) {
    const updateHidden = () => {
      hiddenPin.value = Array.from(pinInputs).map(i => i.value).join('');
    };
    pinInputs.forEach((input, i) => {
      input.addEventListener('input', () => {
        input.value = input.value.replace(/[^0-9]/g, '').slice(0, 1);
        if (input.value && i < pinInputs.length - 1) pinInputs[i + 1].focus();
        updateHidden();
      });
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !input.value && i > 0) pinInputs[i - 1].focus();
      });
    });
  }

  // --- 誕生日を1つのinput（name="birthday"）で受けるページ用 ---
  const birthday = document.querySelector('input[name="birthday"]');
  if (birthday) {
    birthday.addEventListener('input', () => {
      birthday.value = birthday.value.replace(/\D/g, '').slice(0, 4); // 数字のみ4桁
    });
  }
});
