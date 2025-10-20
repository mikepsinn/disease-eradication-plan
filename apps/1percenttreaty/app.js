// 1% Treaty Referendum - Form Submission Logic

// Get referral code from URL if present
const urlParams = new URLSearchParams(window.location.search);
const refCode = urlParams.get('ref');
if (refCode) {
    document.getElementById('referralCode').value = refCode;
}

// Form submission handler
document.getElementById('referendumForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const errorMessage = document.getElementById('errorMessage');
    const originalBtnText = submitBtn.textContent;

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'SUBMITTING...';
    errorMessage.classList.remove('show');

    const formData = {
        fullName: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        country: document.getElementById('country').value,
        referralCode: document.getElementById('referralCode').value
    };

    try {
        // Call Cloudflare Worker
        const response = await fetch('/api/submit-vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Failed to submit vote');
        }

        // Success! Show success message
        document.getElementById('voteForm').style.display = 'none';
        document.getElementById('successMessage').classList.add('show');
        document.getElementById('viralSection').style.display = 'block';
        document.getElementById('displayRefCode').textContent = result.referralCode;

        // Update share links
        updateShareLinks(result.referralCode);

    } catch (error) {
        console.error('Error submitting vote:', error);
        errorMessage.textContent = error.message || 'Something went wrong. Please try again.';
        errorMessage.classList.add('show');
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
    }
});

// Update social share links with referral code
function updateShareLinks(refCode) {
    const baseUrl = window.location.origin + window.location.pathname;
    const shareUrl = `${baseUrl}?ref=${refCode}`;
    const message = "I just voted to redirect 1% of military spending to cure disease. Join me and let's make death optional.";

    // Update share button hrefs
    document.getElementById('shareTwitter').href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}&url=${encodeURIComponent(shareUrl)}`;
    document.getElementById('shareFacebook').href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
    document.getElementById('shareWhatsApp').href = `https://wa.me/?text=${encodeURIComponent(message + ' ' + shareUrl)}`;

    // Add click handlers to open in popup
    document.getElementById('shareTwitter').onclick = function(e) {
        e.preventDefault();
        window.open(this.href, 'share', 'width=550,height=420');
    };
    document.getElementById('shareFacebook').onclick = function(e) {
        e.preventDefault();
        window.open(this.href, 'share', 'width=550,height=420');
    };
}
