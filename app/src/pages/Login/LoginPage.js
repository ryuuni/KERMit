import PageTemplate from '../Template/PageTemplate';
import background from './LoginDesign.svg';

const LoginPage = () => {
  return (
    <PageTemplate>
      <img src={background} alt="ppt background" style={{ objectFit: "cover" }} />
    </PageTemplate>
  );
}

export default LoginPage